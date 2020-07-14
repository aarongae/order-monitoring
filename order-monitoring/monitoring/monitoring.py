from flask import request
from flask import make_response
from flask import Flask
from messages_pb2 import OrderState, OrderUpdate, Report, Time, Overview, NoState, OrderStateWithPrevious, TimeoutReport

from statefun import StatefulFunctions
from statefun import RequestReplyHandler
from statefun import kafka_egress_record
from datetime import timedelta
import typing

functions = StatefulFunctions()


@functions.bind("lieferbot/monitoring")
def monitor(context, order_update: OrderUpdate):

    state = context.state('order_state').unpack(OrderState)
    state_with_previous = OrderStateWithPrevious()
    state_with_previous.status = order_update.status

    if not state:
        state = OrderState()
        state_with_previous.previous = False
    else:
        state_with_previous.previous = True

    state.status = order_update.status
    context.state('order_state').pack(state)

    if state.status == "UNASSIGNED":
        time_unassigned = context.state('time_unassigned').unpack(Time)
        if not time_unassigned:
            time_unassigned = Time()
        time_unassigned.time = order_update.time
        context.state('time_unassigned').pack(time_unassigned)

    elif state.status == "ASSIGNED":
        time_assigned = context.state('time_assigned').unpack(Time)
        if not time_assigned:
            time_assigned = Time()
        time_assigned.time = order_update.time
        context.state('time_assigned').pack(time_assigned)

    elif state.status == "IN_PROGRESS":
        time_in_progress = context.state('time_in_progress').unpack(Time)
        if not time_in_progress:
            time_in_progress = Time()
        time_in_progress.time = order_update.time
        context.state('time_in_progress').pack(time_in_progress)

    elif state.status == "DELIVERED":
        time_delivered = context.state('time_delivered').unpack(Time)
        if not time_delivered:
            time_delivered = Time()
        time_delivered.time = order_update.time
        context.state('time_delivered').pack(time_delivered)

        report = compute_report(context, order_update)

        egress_message = kafka_egress_record(
            topic="reports", key=order_update.id, value=report)
        context.pack_and_send_egress("lieferbot/status", egress_message)

    context.pack_and_send("lieferbot/overview", "overview", state_with_previous)
    context.pack_and_send("lieferbot/timeout_counter", order_update.id, order_update)
    context.pack_and_send("lieferbot/timeout_check", order_update.id, state)


def compute_report(context, order_update: OrderUpdate):
    # Compute the final report, after an order has reached the state delivered
    report = Report()
    report.id = order_update.id
    report.vehicle = order_update.vehicle

    time_unassigned = context.state('time_unassigned').unpack(Time)
    if not time_unassigned:
        time_unassigned = Time()
        time_unassigned.time
    report.timeUnassigned = time_unassigned.time
    context.state('time_unassigned').pack(time_unassigned)

    time_assigned = context.state('time_assigned').unpack(Time)
    if not time_assigned:
        time_assigned = Time()
        time_assigned.time
    report.timeAssigned = time_assigned.time
    context.state('time_assigned').pack(time_assigned)

    time_progress = context.state('time_in_progress').unpack(Time)
    if not time_progress:
        time_progress = Time()
        time_progress.time
    report.timeInProgress = time_progress.time
    context.state('time_in_progress').pack(time_progress)

    time_delivered = context.state('time_delivered').unpack(Time)
    if not time_delivered:
        time_delivered = Time()
        time_delivered.time
    report.timeDelivered = time_delivered.time
    context.state('time_delivered').pack(time_delivered)

    return report


@functions.bind("lieferbot/overview")
def overview(context, state: OrderStateWithPrevious):

    if state.status == "UNASSIGNED":
        no_unassigned = context.state('no_unassigned').unpack(NoState)
        if not no_unassigned:
            no_unassigned = NoState()
            no_unassigned.counter = 1
        else:
            no_unassigned.counter += 1
        context.state('no_unassigned').pack(no_unassigned)

    elif state.status == "ASSIGNED":
        no_unassigned = context.state('no_unassigned').unpack(NoState)
        if no_unassigned and state.previous:
            no_unassigned.counter -= 1
            context.state('no_unassigned').pack(no_unassigned)

        no_assigned = context.state('no_assigned').unpack(NoState)
        if not no_assigned:
            no_assigned = NoState()
            no_assigned.counter = 1
        else:
            no_assigned.counter += 1
        context.state('no_assigned').pack(no_assigned)

    elif state.status == "IN_PROGRESS":
        no_assigned = context.state('no_assigned').unpack(NoState)
        if no_assigned and state.previous:
            no_assigned.counter -= 1
            context.state('no_assigned').pack(no_assigned)

        no_in_progress = context.state('no_in_progress').unpack(NoState)
        if not no_in_progress:
            no_in_progress = NoState()
            no_in_progress.counter = 1
        else:
            no_in_progress.counter += 1
        context.state('no_in_progress').pack(no_in_progress)

    elif state.status == "DELIVERED":
        no_in_progress = context.state('no_in_progress').unpack(NoState)
        if no_in_progress and state.previous:
            no_in_progress.counter -= 1
            context.state('no_in_progress').pack(no_in_progress)

        no_delivered = context.state('no_delivered').unpack(NoState)
        if not no_delivered:
            no_delivered = NoState()
            no_delivered.counter = 1
        else:
            no_delivered.counter += 1
        context.state('no_delivered').pack(no_delivered)

    overview = compute_overview(context)

    egress_message = kafka_egress_record(
        topic="overviews", key="overview", value=overview)
    context.pack_and_send_egress("lieferbot/status", egress_message)


def compute_overview(context):
    # Compute the final report, after an order has reached the state delivered
    overview = Overview()

    no_unassigned = context.state('no_unassigned').unpack(NoState)
    if no_unassigned:
        overview.noUnassigned = no_unassigned.counter
    else:
        overview.noUnassigned = 0

    no_assigned = context.state('no_assigned').unpack(NoState)
    if no_assigned:
        overview.noAssigned = no_assigned.counter
    else:
        overview.noAssigned = 0

    no_in_progress = context.state('no_in_progress').unpack(NoState)
    if no_in_progress:
        overview.noInProgress = no_in_progress.counter
    else:
        overview.noInProgress = 0

    no_delivered = context.state('no_delivered').unpack(NoState)
    if no_delivered:
        overview.noDelivered = no_delivered.counter
    else:
        overview.noDelivered = 0

    return overview


@functions.bind("lieferbot/timeout_counter")
def timeout(context, order_update: OrderUpdate):

    if(order_update.status!="DELIVERED"):
        delay = timedelta(seconds=30)
        context.pack_and_send_after(delay, "lieferbot/timeout_check", order_update.id, order_update)


@functions.bind("lieferbot/timeout_check")
def timeout(context, request: typing.Union[OrderState, OrderUpdate]):

    if isinstance(request, OrderState):
        state = context.state('order_state').unpack(OrderState)
        if not state:
            state = OrderState()
        state.status = request.status
        context.state('order_state').pack(state)

    elif isinstance(request, OrderUpdate):
        state = context.state('order_state').unpack(OrderState)
        if (state.status == request.status):
            report = TimeoutReport()
            report.order.status = state.status
            report.orderId = request.id

            egress_message = kafka_egress_record(
                topic="timeouts", key=request.id, value=report)
            context.pack_and_send_egress("lieferbot/status", egress_message)


handler = RequestReplyHandler(functions)

#
# Serve the endpoint
#

app = Flask(__name__)


@app.route('/statefun', methods=['POST'])
def handle():
    response_data = handler(request.data)
    response = make_response(response_data)
    response.headers.set('Content-Type', 'application/octet-stream')
    return response


if __name__ == "__main__":
    app.run()
