CREATE TABLE `wastages` (
 `id` int(11) NOT NULL AUTO_INCREMENT,
 `raw_material` varchar(255) DEFAULT NULL,
 `raw_material_category` varchar(255) DEFAULT NULL,
 `quantity` varchar(255) DEFAULT NULL,
 `purchase_price` varchar(255) DEFAULT NULL,
 `total_amount` varchar(255) DEFAULT NULL,
 `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
 `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
 PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci

CREATE TABLE `recipes` (
 `id` int(11) NOT NULL AUTO_INCREMENT,
 `shop_name` varchar(255) DEFAULT NULL,
 `material_from` varchar(255) DEFAULT NULL,
 `category` tinyint(1) unsigned NOT NULL DEFAULT 1,
 `recipe_name` varchar(255) DEFAULT NULL,
 `quantity` int(11) DEFAULT NULL,
 `consumption_unit` varchar(255) DEFAULT NULL,
 `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
 `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
 PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci

CREATE TABLE `stocks` (
 `id` int(11) NOT NULL AUTO_INCREMENT,
 `stock_for` varchar(255) DEFAULT NULL,
 `material_name` varchar(255) DEFAULT NULL,
 `category` varchar(255) DEFAULT NULL,
 `material_unit` varchar(255) DEFAULT NULL,
 `quantity` int(11) DEFAULT NULL,
 `comments` varchar(255) DEFAULT NULL,
 `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
 `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
 PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci

CREATE TABLE `vendors` (
 `id` int(11) NOT NULL AUTO_INCREMENT,
 `name` varchar(255) DEFAULT NULL,
 `company` varchar(255) DEFAULT NULL,
 `email` varchar(255) DEFAULT NULL,
 `phone` varchar(255) DEFAULT NULL,
 `address` varchar(255) DEFAULT NULL,
 `city` varchar(255) DEFAULT NULL,
 `state` varchar(255) DEFAULT NULL,
 `country` varchar(255) DEFAULT NULL,
 `tax_number` varchar(255) DEFAULT NULL,
 `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
 `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
 PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci

CREATE TABLE `puchases` (
 `id` int(11) NOT NULL AUTO_INCREMENT,
 `payment_type` varchar(255) DEFAULT NULL,
 `include_delivery_charge` varchar(255) DEFAULT NULL,
 `raw_material_name` varchar(255) DEFAULT NULL,
 `quantity` int(11) DEFAULT NULL,
 `unit` varchar(255) DEFAULT NULL,
 `price_per_unit` varchar(255) DEFAULT NULL,
 `amount` decimal(28,2) DEFAULT NULL,
 `tax_percentage` decimal(28,2) DEFAULT NULL,
 `tax_amount` decimal(28,2) DEFAULT NULL,
 `description` varchar(255) DEFAULT NULL,
 `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
 `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
 PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci

-- for copying and pasting 
CREATE TABLE `bookings` (
 `id` char(36) NOT NULL,
 `booking_number` varchar(40) DEFAULT NULL,
 `no_of_room` tinyint(3) unsigned NOT NULL DEFAULT 0,
 `user_id` char(36) DEFAULT NULL,
 `company_id` char(36) DEFAULT NULL,
 `check_in` date DEFAULT NULL,
 `check_out` date DEFAULT NULL,
 `guest_details` text DEFAULT NULL,
 `guests_details` text DEFAULT NULL,
 `applied_offer_code` longtext DEFAULT NULL,
 `special_request_code` varchar(255) DEFAULT NULL,
 `pet_charge` decimal(28,2) DEFAULT NULL,
 `pet_charge_qty` tinyint(3) unsigned DEFAULT NULL,
 `early_check_in` decimal(28,2) DEFAULT NULL,
 `request_came_from` varchar(100) NOT NULL DEFAULT 'Brand website',
 `request_booking_id` varchar(255) DEFAULT NULL,
 `ota_reservation_code` longtext DEFAULT NULL,
 `ota_guarantee` longtext DEFAULT NULL,
 `apply_tax_exemption` tinyint(1) DEFAULT NULL,
 `tax_exempt_id` varchar(250) DEFAULT NULL,
 `tax_exemption_certificate` varchar(250) DEFAULT NULL,
 `saved_card_id` varchar(255) DEFAULT NULL,
 `unit_fares` longtext DEFAULT NULL,
 `rate_plans` longtext DEFAULT NULL,
 `rate_templates` longtext DEFAULT NULL,
 `room_type_id` char(36) DEFAULT NULL,
 `tax_charge` decimal(28,8) NOT NULL DEFAULT 0.00000000,
 `taxes` longtext DEFAULT NULL,
 `booking_fare` decimal(28,8) NOT NULL DEFAULT 0.00000000 COMMENT 'Total of room * nights fare ',
 `service_cost` decimal(28,8) NOT NULL DEFAULT 0.00000000,
 `extra_charge` decimal(28,8) NOT NULL DEFAULT 0.00000000,
 `extra_charge_subtracted` decimal(28,8) NOT NULL DEFAULT 0.00000000,
 `paid_amount` decimal(28,8) NOT NULL DEFAULT 0.00000000,
 `cancellation_fee` decimal(28,8) NOT NULL DEFAULT 0.00000000,
 `refunded_amount` decimal(28,8) NOT NULL DEFAULT 0.00000000,
 `key_status` tinyint(1) NOT NULL DEFAULT 0,
 `status` tinyint(1) unsigned NOT NULL DEFAULT 0 COMMENT '1= success/active; 3 = cancelled; 4 = No show; 9 = checked Out',
 `business_source` varchar(100) DEFAULT NULL,
 `checked_in_at` datetime DEFAULT NULL,
 `checked_out_at` datetime DEFAULT NULL,
 `night_audit_void_type` varchar(100) DEFAULT NULL,
 `is_night_audit_completed` tinyint(1) NOT NULL DEFAULT 0 COMMENT '0 = Pending; 1 = In progress; 2 = Completed',
 `id_front` varchar(255) DEFAULT NULL,
 `id_back` varchar(255) DEFAULT NULL,
 `audit_date` date DEFAULT NULL,
 `created_at` timestamp NULL DEFAULT NULL,
 `updated_at` timestamp NULL DEFAULT NULL,
 `govt_id` varchar(255) DEFAULT NULL,
 `govt_id_number` varchar(255) DEFAULT NULL,
 `booking_type` varchar(50) NOT NULL DEFAULT 'Walk In',
 `check_in_completed` tinyint(1) NOT NULL DEFAULT 0,
 `reservation_comments` varchar(300) DEFAULT NULL,
 `internal_comments` varchar(300) DEFAULT NULL,
 `cancellation_reason` varchar(255) DEFAULT NULL,
 `ota_reservation_log` longtext DEFAULT NULL,
 PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci


-- 09-04 pms query
CREATE TABLE `raw_materials` (
 `id` char(36) NOT NULL,
 `material_name` varchar(255) DEFAULT NULL,
 `quantity` int(11) DEFAULT NULL,
 `raw_material_category` varchar(255) DEFAULT NULL,
 `description` varchar(255) DEFAULT NULL,
 `purchase_unit` int(11) DEFAULT NULL,
 `consumption_unit` varchar(255) DEFAULT NULL,
 `conversion_ratio` varchar(255) DEFAULT NULL,
 `price_per_unit` varchar(255) DEFAULT NULL,
 `tax` varchar(255) DEFAULT NULL,
 `expected_wastage` varchar(255) DEFAULT NULL,
 `minimum_stock` varchar(255) DEFAULT NULL,
 `minimum_stock_unit` varchar(255) DEFAULT NULL,
 `at_par_stock` varchar(255) DEFAULT NULL,
 `at_par_unit_stock` varchar(255) DEFAULT NULL,
 `material_code` varchar(255) DEFAULT NULL,
 `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
 `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
 PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci


CREATE TABLE `stock_products` (
 `id` char(36) NOT NULL,
 `name` varchar(250) DEFAULT NULL,
 `code` varchar(250) DEFAULT NULL,
 `description` varchar(255) DEFAULT NULL,
 `category_id` char(36) NOT NULL,
 `unit` enum('pcs', 'set', 'liters') DEFAULT 'pcs',
 `purchase_price` decimal(28,8) NOT NULL DEFAULT 0.00000000,
 `purchase_date` date DEFAULT NULL,
 `warranty` varchar(250) DEFAULT NULL,
 `quantity` int(11) DEFAULT NULL,
 `status` enum('In Use', 'In Stock', 'Under Maintenance','Disposed') DEFAULT 'In Use',
 `created_by` char(36) DEFAULT NULL,
 `updated_by` char(36) DEFAULT NULL,
 `created_at` timestamp NULL DEFAULT NULL,
 `updated_at` timestamp NULL DEFAULT NULL,
 PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci

CREATE TABLE `stock_vendors` (
 `id` char(36) NOT NULL,
 `vendor_name` varchar(250) DEFAULT NULL,
 `person_email` varchar(250) DEFAULT NULL,
 `person_phone` varchar(250) DEFAULT NULL,
 `tax_details` varchar(250) DEFAULT NULL,
 `payments_terms` varchar(250) DEFAULT NULL,
 `notes` varchar(250) DEFAULT NULL,
 `created_by` char(36) DEFAULT NULL,
 `updated_by` char(36) DEFAULT NULL,
 `created_at` timestamp NULL DEFAULT NULL,
 `updated_at` timestamp NULL DEFAULT NULL,
 PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci
