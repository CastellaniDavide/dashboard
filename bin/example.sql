INSERT INTO `machine` (`mac`, `machine_name`, `os`, `os_version`, `DHCP`, `TIMESTAMP`) VALUES ('10-10-20-30-43-25', 'machine1', 'windows', '10', BIN('1'), '09:42:35');

INSERT INTO `business_value` (`NAME`, `priority`, `TIMESTAMP`) VALUES ('example', '7', '10:04:39');

INSERT INTO `services` (`id`, `service`, `PORT`, `mac_id`, `business_value`) VALUES ('0', ' example_test', '8080', '10-10-20-30-43-25', 'example');

INSERT INTO `test` (`id`, `priority`, `service`) VALUES ('0', '6', 'example_service');

INSERT INTO `test_services` (`test_id`, `service_id`, `extra`) VALUES ('0', '0', NULL);