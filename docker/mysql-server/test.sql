/*!40101 SET character_set_client = utf8 */;
USE `findme`;

DROP TABLE IF EXISTS `actions`;
CREATE TABLE `actions` (
  `aid` varchar(255) NOT NULL DEFAULT '0' COMMENT 'Primary Key: Unique actions ID.',
  `type` varchar(32) NOT NULL DEFAULT '' COMMENT 'The object that that action acts on (node, user, comment, system or custom types.)',
  `callback` varchar(255) NOT NULL DEFAULT '' COMMENT 'The callback function that executes when the action runs.',
  `parameters` longblob NOT NULL COMMENT 'Parameters to be passed to the callback function.',
  `label` varchar(255) NOT NULL DEFAULT '0' COMMENT 'Label of the action.',
  PRIMARY KEY (`aid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Stores action information.';

LOCK TABLES `actions` WRITE;
INSERT INTO `actions` VALUES ('comment_publish_action','comment','comment_publish_action','','Publish comment'),('comment_save_action','comment','comment_save_action','','Save comment'),('comment_unpublish_action','comment','comment_unpublish_action','','Unpublish comment'),('node_export_drupal_action','node','node_export_drupal_action','','Node export (Drupal var export)'),('node_make_sticky_action','node','node_make_sticky_action','','Make content sticky'),('node_make_unsticky_action','node','node_make_unsticky_action','','Make content unsticky'),('node_promote_action','node','node_promote_action','','Promote content to front page'),('node_publish_action','node','node_publish_action','','Publish content'),('node_save_action','node','node_save_action','','Save content'),('node_unpromote_action','node','node_unpromote_action','','Remove content from front page'),('node_unpublish_action','node','node_unpublish_action','','Unpublish content'),('pathauto_node_update_action','node','pathauto_node_update_action','','Update node alias'),('pathauto_taxonomy_term_update_action','taxonomy_term','pathauto_taxonomy_term_update_action','','Update taxonomy term alias'),('pathauto_user_update_action','user','pathauto_user_update_action','','Update user alias'),('replicate_ui_replicate_item','entity','replicate_ui_replicate_item','','Replicate item'),('system_block_ip_action','user','system_block_ip_action','','Ban IP address of current user'),('user_block_user_action','user','user_block_user_action','','Block current user'),('views_bulk_operations_archive_action','file','views_bulk_operations_archive_action','','Create an archive of selected files'),('views_bulk_operations_argument_selector_action','entity','views_bulk_operations_argument_selector_action','','Pass ids as arguments to a page'),('views_bulk_operations_delete_item','entity','views_bulk_operations_delete_item','','Delete item'),('views_bulk_operations_delete_revision','entity','views_bulk_operations_delete_revision','','Delete revision'),('views_bulk_operations_modify_action','entity','views_bulk_operations_modify_action','','Modify entity values');
UNLOCK TABLES;

DROP TABLE IF EXISTS `tbl_users`;

CREATE TABLE `tbl_users` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT 'Primary Key: ',
  `user_id` varchar(255) NOT NULL DEFAULT '0' COMMENT 'Primary Key: Unique user ID.',
  `email` varchar(255) NOT NULL DEFAULT '' COMMENT 'User Email',
  `first_name` varchar(255) NOT NULL DEFAULT '' COMMENT 'User First Name',
  `last_name` varchar(255) NOT NULL DEFAULT '' COMMENT 'User Last Name',
  `password`  varchar(255) NOT NULL DEFAULT '' COMMENT 'User pasword',
  `organization` varchar(255) NOT NULL DEFAULT '' COMMENT 'User Company or Organization',
  `designation` varchar(255) NOT NULL DEFAULT '' COMMENT 'User Title or Designation',
  `location_latitude` varchar(255) NOT NULL DEFAULT '' COMMENT 'User Geocoordinate Latitude',
  `location_longitude` varchar(255) NOT NULL DEFAULT '' COMMENT 'User Geocoordinate Longitude',
  `profile_picture` varchar(255) NOT NULL DEFAULT '' COMMENT 'Profile Pic URL',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Stores user information.';

LOCK TABLES `tbl_users` WRITE;
INSERT INTO `tbl_users` VALUES ('1', 'mtaylor769', 'mike@whatsmycut.com', 'Mike', 'Taylor', '', 'WMCP', 'Owner', '', '', '');
INSERT INTO `tbl_users` VALUES ('2', 'user2', 'user@whatsmycut.com', 'Default', 'User', '', 'ACME Co.', 'Employee', '', '', '');
UNLOCK TABLES;


DROP TABLE IF EXISTS `tbl_contacts`;
CREATE TABLE `tbl_contacts` (
 `user_id` int NOT NULL DEFAULT 0 COMMENT='Current User ID',
 `contact_id` int NOT NULL DEFAULT 0 COMMENT='Contact User ID',
 `status` boolean NOT NULL DEFAULT 'false' COMMENT='True is connected.',
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Stores user contact relationships.';

LOCK TABLES `tbl_contacts` WRITE;
INSERT INTO `tbl_contacts` VALUES (1, 2, 1);
UNLOCK TABLES;

DROP TABLE IF EXISTS `tbl_groups`;
CREATE TABLE `tbl_groups` (
  `id`
  `group_name` varchar(255) NOT NULL DEFAULT '' COMMENT 'Group Name',
  `group_picture`  varchar(255) NOT NULL DEFAULT '' COMMENT 'Group Picture',
  `owner` varchar(255) NOT NULL DEFAULT '' COMMENT 'Group Owner',
  `member_invite_contact` varchar(255) NOT NULL DEFAULT '' COMMENT 'Group invitations sent to',
  `password` varchar(255) NOT NULL DEFAULT '' COMMENT 'Group password',
  `phone`  varchar(255) NOT NULL DEFAULT '' COMMENT 'Group phone number',
  `email` varchar(255) NOT NULL DEFAULT '' COMMENT 'Group email',
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Stores Group information';
