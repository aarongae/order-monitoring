from flask import request
from flask import make_response
from flask import Flask
from messages_pb2 import OrderState, OrderUpdate, OrderStatus, Time, Report

from statefun import StatefulFunctions
from statefun import RequestReplyHandler
from statefun import kafka_egress_record

from datetime import datetime
import time


functions = StatefulFunctions()


@functions.bind("lieferbot/monitoring")
def monitore(context, order_update: OrderUpdate):
    state = context.state('order_state').unpack(OrderState)
    if not state:
        state = OrderState()
        state.state = 0
    else:
        state.state += 1
    context.state('order_state').pack(state)

    response = compute_status(order_update.id, state.state)
    compute_time(context, order_update)

    egress_message = kafka_egress_record(
        topic="status", key=order_update.id, value=response)
    context.pack_and_send_egress("lieferbot/status", egress_message)


def compute_time(context, order_update: OrderUpdate):

    state = context.state('order_state').unpack(OrderState)

    if state.state == 0:
        timeunassigned = context.state('time_unassigned').unpack(Time)
        if not timeunassigned:
            t = time.time()
            timeunassigned = Time()
            timeunassigned.time = t
        context.state('time_unassigned').pack(timeunassigned)

    elif state.state == 1:
        timeassigned = context.state('time_assigned').unpack(Time)
        t = time.time()
        timeassigned = Time()
        timeassigned.time = t
        context.state('time_assigned').pack(timeassigned)

    elif state.state == 2:
        timeprogress = context.state('time_in_progress').unpack(Time)
        if not timeprogress:
            t = time.time()
            timeprogress = Time()
            timeprogress.time = t
        context.state('time_in_progress').pack(timeprogress)

    elif state.state == 3:
        timedelivered = context.state('time_delivered').unpack(Time)
        if not timedelivered:
            t = time.time()
            timedelivered = Time()
            timedelivered.time = t

        context.state('time_delivered').pack(timedelivered)

        response = Report()
        response.id = order_update.id
        response.vehicle = -1

        timeunassigned = context.state('time_unassigned').unpack(Time)
        response.timeUnassigned = timeunassigned.time
        context.state('time_unassigned').pack(timeunassigned)

        timeassigned = context.state('time_assigned').unpack(Time)
        response.timeAssigned = timeassigned.time
        context.state('time_assigned').pack(timeassigned)

        timeprogress = context.state('time_in_progress').unpack(Time)
        response.timeInProgress = timeprogress.time
        context.state('time_in_progress').pack(timeprogress)

        timedelivered = context.state('time_delivered').unpack(Time)
        response.timeDelivered = timedelivered.time
        context.state('time_delivered').pack(timedelivered)

        egress_message = kafka_egress_record(
            topic="reports", value=response)
        context.pack_and_send_egress("lieferbot/status", egress_message)

    context.state('order_state').pack(state)


def compute_status(id, state):
    """
    Compute order status based on @state
    """
    now = datetime.now()

    if state == 0:
        status = "Order:%s Status:UNASSIGNED Time:%s" % (
            id, now.strftime("%d.%m.%Y - %H:%M:%S"))
    elif state == 1:
        status = "Order:%s Status:ASSIGNED Time:%s" % (
            id, now.strftime("%d.%m.%Y - %H:%M:%S"))
    elif state == 2:
        status = "Order:%s Status:IN_PROGRESS Time:%s" % (
            id, now.strftime("%d.%m.%Y - %H:%M:%S"))
    elif state == 3:
        status = "Order:%s Status:DELIVERED Time:%s" % (
            id, now.strftime("%d.%m.%Y - %H:%M:%S"))
    else:
        status = "Order:%s Status:UNKNOWN Time:%s" % (
            id, now.strftime("%d.%m.%Y - %H:%M:%S"))

    response = OrderStatus()
    response.id = id
    response.status = status

    return response


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
