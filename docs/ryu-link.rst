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

Secondly, some data must be sent by the controller in order to use some modules of TouSIX-Manager.
You can find a basic implementation of these datas in the Ryu apps furnished with the project.