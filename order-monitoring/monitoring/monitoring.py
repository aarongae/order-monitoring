from flask import request
from flask import make_response
from flask import Flask
from messages_pb2 import OrderState, OrderUpdate, Report, Time

from statefun import StatefulFunctions
from statefun import RequestReplyHandler
from statefun import kafka_egress_record

from datetime import datetime
import time

functions = StatefulFunctions()


@functions.bind("lieferbot/monitoring")
def monitor(context, order_update: OrderUpdate):

    state = context.state('order_state').unpack(OrderState)
    if not state:
        state = OrderState()
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
            topic="reports",  key=order_update.id, value=report)
        context.pack_and_send_egress("lieferbot/status", egress_message)

    
def compute_report(context, order_update: OrderUpdate):
    # Compute the final report, after an order has reached the state delivered
    report = Report()
    report.id = order_update.id
    report.vehicle = order_update.vehicle

    time_unassigned = context.state('time_unassigned').unpack(Time)
    report.timeUnassigned = time_unassigned.time
    context.state('time_unassigned').pack(time_unassigned)

    time_assigned = context.state('time_assigned').unpack(Time)
    report.timeAssigned = time_assigned.time
    context.state('time_assigned').pack(time_assigned)

    time_progress = context.state('time_in_progress').unpack(Time)
    report.timeInProgress = time_progress.time
    context.state('time_in_progress').pack(time_progress)

    time_delivered = context.state('time_delivered').unpack(Time)
    report.timeDelivered = time_delivered.time
    context.state('time_delivered').pack(time_delivered)

    return report


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
