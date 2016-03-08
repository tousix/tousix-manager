Linkage with Ryu controller
===========================

TouSIX-Manager can not modify any OpenFlow topology on its own.
It need the help of a OpenFlow controller to complete the program.

Using Ryu as an OpenFlow controller is not an absolute requirement.
Currently, the support is only limited to this program.
But theoretically, any controller should work.
They must match two requirements.
First is to implement a REST API similar to the Ryu one:

http://ryu.readthedocs.org/en/latest/app/ofctl_rest.html

This is essential to permit TouSIX-Manager for manage your topology without having a strong dependence on a specific controller.

Secondly, some data must be sent by the controller in order to use some modules of TouSIX-Manager.
TouSIX-Manager expect to receive a POST response, with a fixed structure in these parameters.
We can represent these parameters in JSON like the following example (for the statistics app):
::

    {"time": "2014-07-14T19:43:37+0100",  // ISO 8601 format
     "dpid_switch": [
     {"byte_count": 23652694,
      "packet_count": 456568,
      "cookie": 4428111283215}
      ]}
Other fields added in the parameters will be ignored.

You can find a basic implementation of these datas in the Ryu apps furnished with the project.