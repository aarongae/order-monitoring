# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: messages.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='messages.proto',
  package='lieferbot',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=b'\n\x0emessages.proto\x12\tlieferbot\"*\n\x0bOrderUpdate\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0f\n\x07vehicle\x18\x02 \x01(\x03\")\n\x0bOrderStatus\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0e\n\x06status\x18\x02 \x01(\t\"\x89\x01\n\nOrderState\x12\x30\n\x06status\x18\x02 \x01(\x0e\x32 .lieferbot.OrderState.StatusType\"I\n\nStatusType\x12\x0e\n\nUNASSIGNED\x10\x00\x12\x0c\n\x08\x41SSIGNED\x10\x01\x12\x0e\n\nINPROGRESS\x10\x02\x12\r\n\tDELIVERED\x10\x03\"\x14\n\x04Time\x12\x0c\n\x04time\x18\x01 \x01(\x02\"\x82\x01\n\x06Report\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0f\n\x07vehicle\x18\x02 \x01(\x03\x12\x16\n\x0etimeUnassigned\x18\x03 \x01(\x02\x12\x14\n\x0ctimeAssigned\x18\x04 \x01(\x02\x12\x16\n\x0etimeInProgress\x18\x05 \x01(\x02\x12\x15\n\rtimeDelivered\x18\x06 \x01(\x02\x62\x06proto3'
)



_ORDERSTATE_STATUSTYPE = _descriptor.EnumDescriptor(
  name='StatusType',
  full_name='lieferbot.OrderState.StatusType',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='UNASSIGNED', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ASSIGNED', index=1, number=1,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='INPROGRESS', index=2, number=2,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='DELIVERED', index=3, number=3,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=181,
  serialized_end=254,
)
_sym_db.RegisterEnumDescriptor(_ORDERSTATE_STATUSTYPE)


_ORDERUPDATE = _descriptor.Descriptor(
  name='OrderUpdate',
  full_name='lieferbot.OrderUpdate',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='lieferbot.OrderUpdate.id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='vehicle', full_name='lieferbot.OrderUpdate.vehicle', index=1,
      number=2, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=29,
  serialized_end=71,
)


_ORDERSTATUS = _descriptor.Descriptor(
  name='OrderStatus',
  full_name='lieferbot.OrderStatus',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='lieferbot.OrderStatus.id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='status', full_name='lieferbot.OrderStatus.status', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=73,
  serialized_end=114,
)


_ORDERSTATE = _descriptor.Descriptor(
  name='OrderState',
  full_name='lieferbot.OrderState',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='status', full_name='lieferbot.OrderState.status', index=0,
      number=2, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _ORDERSTATE_STATUSTYPE,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=117,
  serialized_end=254,
)


_TIME = _descriptor.Descriptor(
  name='Time',
  full_name='lieferbot.Time',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='time', full_name='lieferbot.Time.time', index=0,
      number=1, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=256,
  serialized_end=276,
)


_REPORT = _descriptor.Descriptor(
  name='Report',
  full_name='lieferbot.Report',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='lieferbot.Report.id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='vehicle', full_name='lieferbot.Report.vehicle', index=1,
      number=2, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='timeUnassigned', full_name='lieferbot.Report.timeUnassigned', index=2,
      number=3, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='timeAssigned', full_name='lieferbot.Report.timeAssigned', index=3,
      number=4, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='timeInProgress', full_name='lieferbot.Report.timeInProgress', index=4,
      number=5, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='timeDelivered', full_name='lieferbot.Report.timeDelivered', index=5,
      number=6, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=279,
  serialized_end=409,
)

_ORDERSTATE.fields_by_name['status'].enum_type = _ORDERSTATE_STATUSTYPE
_ORDERSTATE_STATUSTYPE.containing_type = _ORDERSTATE
DESCRIPTOR.message_types_by_name['OrderUpdate'] = _ORDERUPDATE
DESCRIPTOR.message_types_by_name['OrderStatus'] = _ORDERSTATUS
DESCRIPTOR.message_types_by_name['OrderState'] = _ORDERSTATE
DESCRIPTOR.message_types_by_name['Time'] = _TIME
DESCRIPTOR.message_types_by_name['Report'] = _REPORT
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

OrderUpdate = _reflection.GeneratedProtocolMessageType('OrderUpdate', (_message.Message,), {
  'DESCRIPTOR' : _ORDERUPDATE,
  '__module__' : 'messages_pb2'
  # @@protoc_insertion_point(class_scope:lieferbot.OrderUpdate)
  })
_sym_db.RegisterMessage(OrderUpdate)

OrderStatus = _reflection.GeneratedProtocolMessageType('OrderStatus', (_message.Message,), {
  'DESCRIPTOR' : _ORDERSTATUS,
  '__module__' : 'messages_pb2'
  # @@protoc_insertion_point(class_scope:lieferbot.OrderStatus)
  })
_sym_db.RegisterMessage(OrderStatus)

OrderState = _reflection.GeneratedProtocolMessageType('OrderState', (_message.Message,), {
  'DESCRIPTOR' : _ORDERSTATE,
  '__module__' : 'messages_pb2'
  # @@protoc_insertion_point(class_scope:lieferbot.OrderState)
  })
_sym_db.RegisterMessage(OrderState)

Time = _reflection.GeneratedProtocolMessageType('Time', (_message.Message,), {
  'DESCRIPTOR' : _TIME,
  '__module__' : 'messages_pb2'
  # @@protoc_insertion_point(class_scope:lieferbot.Time)
  })
_sym_db.RegisterMessage(Time)

Report = _reflection.GeneratedProtocolMessageType('Report', (_message.Message,), {
  'DESCRIPTOR' : _REPORT,
  '__module__' : 'messages_pb2'
  # @@protoc_insertion_point(class_scope:lieferbot.Report)
  })
_sym_db.RegisterMessage(Report)


# @@protoc_insertion_point(module_scope)
