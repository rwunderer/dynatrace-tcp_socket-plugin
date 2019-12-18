from ruxit.api.base_plugin import RemoteBasePlugin
import logging
import socket

logger = logging.getLogger(__name__)

class TcpSocketPluginRemote(RemoteBasePlugin):
	def initialize(self, **kwargs):
		logger.info("Config: %s", self.config)
		self.address = self.config["address"]
		self.port = self.config["port"]
		self.device_name = self.config["device_name"]
		self.device_display_name = self.config["device_display_name"]

	def query(self, **kwargs):
		# Create group - provide group id used to calculate unique entity id in dynatrace
		#   and display name for UI presentation
		group = self.topology_builder.create_group(identifier="TCP",
												   group_name="TCP connections")

		# Create device - provide device id used to calculate unique entity id in dynatrace
		#   and display name for UI presentation
		device = group.create_device(identifier=self.device_name,
									 display_name=self.device_display_name)
		device.add_endpoint(ip=self.address, port=self.port)

		logger.info("Topology: group name=%s, device name=%s", group.name, device.name)

		# Check socket
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.settimeout(1)

		try:
			s.connect((self.address, self.port))
			device.state_metric(key='state', value='OK')
			logger.info("Connection to %s:%d OK." % (self.address, self.port))
			s.shutdown(socket.SHUT_RDWR)

		except Exception as e:
			device.state_metric(key='state', value='ERROR')
			device.report_availability_event(title="%s unavailable" % (self.device_display_name),
											 description="Couldn't connect to %s:%d: %s." % (self.address, self.port, e),
											 properties={"current_timeout": "1s"})
			logger.info("Couldn't connect to %s:%d: %s." % (self.address, self.port, e))

		finally:
			s.close()
