CREATE TABLE users (
	id INTEGER NOT NULL, 
	email VARCHAR(255) NOT NULL, 
	password_hash VARCHAR(255) NOT NULL, 
	full_name VARCHAR(120) NOT NULL, 
	phone VARCHAR(30), 
	role VARCHAR(20) NOT NULL, 
	created_at TIMESTAMP NOT NULL, 
	PRIMARY KEY (id)
);
INSERT INTO users VALUES(1,'s5618448@bournemouth.ac.uk','scrypt:32768:8:1$God0SnrwQ81kQiwQ$f59fe6692c314261aa5ae65ef2a09fd2601010691026dd546e1ae4a5e51511bd4d763edf223b75895a6f14a128694e61930f3817f72feea77cf9c9b9b9837b9d','Joshua Cardozo','07438387592','customer','2026-01-25 01:29:52.802235');
INSERT INTO users VALUES(2,'rachel16@ggmail.com','scrypt:32768:8:1$sDZWbT4pAGD8PbgD$4268ce7ae44a39715fd28ce77f8d8227419d96ea8f4a2a848f7454cb2019c5b0f7dd39f16a481ae62fee6acb8063d6c81b7f0d37af1d2dff1cbec98a6ba1e8cc','RACHEL',NULL,'customer','2026-01-25 01:43:29.637800');
INSERT INTO users VALUES(3,'joshcardozo16@gmail.com','scrypt:32768:8:1$k2Lzm5YkTxkCqfL8$573216689c43f11d14a33dbe8bf0dbbacc4677928e0c051dcce90c56632c3f104bdae66f01ff98f26faee5f3df955ed3f2a78fe4ea63550aef239e540d11e896','Joshua Cardozo','07440182311','admin','2026-01-25 02:11:50.425290');
INSERT INTO users VALUES(4,'customer1@gmail.com','scrypt:32768:8:1$rn6c3tNg0wFAIIMy$3370bdf8dc72a67c33c0147388248d82427842da693805471259f7928e52d07ff9d61cee1b173280d3e7867f6ff86eb25b83560684d1f9638614df0c914cdee2','customer1',NULL,'customer','2026-01-28 23:20:24.057706');
CREATE TABLE menu_items (
	id INTEGER NOT NULL, 
	name VARCHAR(120) NOT NULL, 
	description TEXT, 
	price NUMERIC(10, 2) NOT NULL, 
	category VARCHAR(50) NOT NULL, 
	image_url VARCHAR(500), 
	is_available BOOLEAN NOT NULL, 
	created_at TIMESTAMP NOT NULL, 
	PRIMARY KEY (id)
);
INSERT INTO menu_items VALUES(1,'Saffron Chicken Tikka Skewers','Chargrilled skewers, mint yoghurt, lemon.',7.950000000000000177,'Starters','https://images.unsplash.com/photo-1604908176997-125f25cc500f?auto=format&fit=crop&w=1200&q=80',1,'2026-01-26 01:21:16.186663');
INSERT INTO menu_items VALUES(2,'Smoked Paprika Halloumi Fries','Crispy halloumi fries, chilli honey dip.',6.5,'Starters','https://images.unsplash.com/photo-1541592106381-b31e9677c0e5?auto=format&fit=crop&w=1200&q=80',1,'2026-01-26 01:21:16.186667');
INSERT INTO menu_items VALUES(3,'Spiced Lentil Soup','Slow-cooked lentils, cumin, herbs.',5.950000000000000177,'Starters','https://images.unsplash.com/photo-1543353071-087092ec393a?auto=format&fit=crop&w=1200&q=80',1,'2026-01-26 01:21:16.186668');
INSERT INTO menu_items VALUES(4,'Garlic & Herb Flatbread','Warm flatbread with garlic butter.',4.950000000000000177,'Starters','https://images.unsplash.com/photo-1601050690597-df0568f70950?auto=format&fit=crop&w=1200&q=80',1,'2026-01-26 01:21:16.186669');
INSERT INTO menu_items VALUES(5,'Crispy Calamari','Lightly fried calamari, lemon aioli.',7.5,'Starters','https://images.unsplash.com/photo-1559847844-5315695dadae?auto=format&fit=crop&w=1200&q=80',1,'2026-01-26 01:21:16.186670');
INSERT INTO menu_items VALUES(6,'Sharer Platter (Mix Grill)','Chicken tikka, lamb kofta, halloumi, salad, dips.',19.94999999999999929,'Sharers','https://images.unsplash.com/photo-1555939594-58d7cb561ad1?auto=format&fit=crop&w=1200&q=80',1,'2026-01-26 01:21:16.186671');
INSERT INTO menu_items VALUES(7,'Loaded Nachos Sharer','Cheese, salsa, jalapeños, sour cream.',11.94999999999999929,'Sharers','https://images.unsplash.com/photo-1543339318-b43dc53e19b3?auto=format&fit=crop&w=1200&q=80',1,'2026-01-26 01:21:16.186672');
INSERT INTO menu_items VALUES(8,'Wings Sharer (12 pcs)','Choose: BBQ / Hot / Garlic. Served with dip.',12.94999999999999929,'Sharers','https://images.unsplash.com/photo-1604908176997-125f25cc500f?auto=format&fit=crop&w=1200&q=80',1,'2026-01-26 01:21:16.186673');
INSERT INTO menu_items VALUES(9,'Chargrilled Lamb Kofta','Kofta, warm flatbread, salad, tahini.',15.94999999999999929,'Mains','https://images.unsplash.com/photo-1555939594-58d7cb561ad1?auto=format&fit=crop&w=1200&q=80',1,'2026-01-26 01:21:16.186674');
INSERT INTO menu_items VALUES(10,'Butter Chicken Masala','Creamy tomato curry, served with rice.',14.5,'Mains','https://images.unsplash.com/photo-1604908176997-125f25cc500f?auto=format&fit=crop&w=1200&q=80',1,'2026-01-26 01:21:16.186675');
INSERT INTO menu_items VALUES(11,'Paneer Tikka Curry','Spiced paneer curry, peppers, onions, rice.',13.94999999999999929,'Mains','https://images.unsplash.com/photo-1601050690597-df0568f70950?auto=format&fit=crop&w=1200&q=80',1,'2026-01-26 01:21:16.186676');
INSERT INTO menu_items VALUES(12,'Smoky BBQ Ribs','Half rack ribs, BBQ glaze, slaw.',16.94999999999999929,'Mains','https://images.unsplash.com/photo-1544025162-d76694265947?auto=format&fit=crop&w=1200&q=80',1,'2026-01-26 01:21:16.186676');
INSERT INTO menu_items VALUES(13,'Grilled Salmon Bowl','Salmon, herbs, seasonal veg, rice.',15.5,'Mains','https://images.unsplash.com/photo-1467003909585-2f8a72700288?auto=format&fit=crop&w=1200&q=80',1,'2026-01-26 01:21:16.186677');
INSERT INTO menu_items VALUES(14,'Veg Tagine','Slow-cooked veg, chickpeas, spices, couscous.',12.94999999999999929,'Mains','https://images.unsplash.com/photo-1512621776951-a57141f2eefd?auto=format&fit=crop&w=1200&q=80',1,'2026-01-26 01:21:16.186678');
INSERT INTO menu_items VALUES(15,'Burger Meal Deal','Any burger + fries + soft drink (save vs buying separately).',15.94999999999999929,'Meal Deals','https://images.unsplash.com/photo-1550547660-d9450f859349?auto=format&fit=crop&w=1200&q=80',1,'2026-01-26 01:21:16.186679');
INSERT INTO menu_items VALUES(16,'Rice Bowl Meal Deal','Any rice bowl + side + soft drink (value deal).',15.5,'Meal Deals','https://images.unsplash.com/photo-1540189549336-e6e99c3679fe?auto=format&fit=crop&w=1200&q=80',1,'2026-01-26 01:21:16.186680');
INSERT INTO menu_items VALUES(17,'Wrap Meal Deal','Any wrap + fries + soft drink (customer favourite).',13.94999999999999929,'Meal Deals','https://images.unsplash.com/photo-1523986371872-9d3ba2e2f642?auto=format&fit=crop&w=1200&q=80',1,'2026-01-26 01:21:16.186681');
INSERT INTO menu_items VALUES(18,'Saffron Rice Bowl – Chicken','Saffron rice, grilled chicken, salad, house sauce.',12.94999999999999929,'Rice Combos','https://images.unsplash.com/photo-1540189549336-e6e99c3679fe?auto=format&fit=crop&w=1200&q=80',1,'2026-01-26 01:21:16.186681');
INSERT INTO menu_items VALUES(19,'Saffron Rice Bowl – Lamb','Saffron rice, lamb kofta, pickles, tahini drizzle.',13.94999999999999929,'Rice Combos','https://images.unsplash.com/photo-1555939594-58d7cb561ad1?auto=format&fit=crop&w=1200&q=80',1,'2026-01-26 01:21:16.186682');
INSERT INTO menu_items VALUES(20,'Saffron Rice Bowl – Veg','Saffron rice, roasted veg, chickpeas, garlic sauce.',11.94999999999999929,'Rice Combos','https://images.unsplash.com/photo-1512621776951-a57141f2eefd?auto=format&fit=crop&w=1200&q=80',1,'2026-01-26 01:21:16.186683');
INSERT INTO menu_items VALUES(21,'Spicy Chicken Rice Box','Spiced chicken, rice, salad, chilli mayo.',12.5,'Rice Combos','https://images.unsplash.com/photo-1540189549336-e6e99c3679fe?auto=format&fit=crop&w=1200&q=80',1,'2026-01-26 01:21:16.186684');
INSERT INTO menu_items VALUES(22,'Teriyaki Veg Rice Box','Veg, teriyaki glaze, sesame, rice.',11.5,'Rice Combos','https://images.unsplash.com/photo-1512621776951-a57141f2eefd?auto=format&fit=crop&w=1200&q=80',1,'2026-01-26 01:21:16.186685');
INSERT INTO menu_items VALUES(23,'Chicken Tikka Wrap','Chicken tikka, salad, mint yoghurt, wrap.',10.94999999999999928,'Wraps','https://images.unsplash.com/photo-1523986371872-9d3ba2e2f642?auto=format&fit=crop&w=1200&q=80',1,'2026-01-26 01:21:16.186686');
INSERT INTO menu_items VALUES(24,'Lamb Kofta Wrap','Lamb kofta, pickles, tahini, wrap.',11.94999999999999929,'Wraps','https://images.unsplash.com/photo-1555939594-58d7cb561ad1?auto=format&fit=crop&w=1200&q=80',1,'2026-01-26 01:21:16.186687');
INSERT INTO menu_items VALUES(25,'Falafel & Hummus Wrap','Falafel, hummus, salad, garlic sauce.',9.94999999999999928,'Wraps','https://images.unsplash.com/photo-1512621776951-a57141f2eefd?auto=format&fit=crop&w=1200&q=80',1,'2026-01-26 01:21:16.186687');
INSERT INTO menu_items VALUES(26,'Saffron Smash Burger','Double beef, cheddar, onions, house sauce.',12.94999999999999929,'Burgers','https://images.unsplash.com/photo-1550547660-d9450f859349?auto=format&fit=crop&w=1200&q=80',1,'2026-01-26 01:21:16.186688');
INSERT INTO menu_items VALUES(27,'Smoked BBQ Chicken Burger','Smoked chicken, slaw, pickles, BBQ glaze.',12.5,'Burgers','https://images.unsplash.com/photo-1550317138-10000687a72b?auto=format&fit=crop&w=1200&q=80',1,'2026-01-26 01:21:16.186689');
INSERT INTO menu_items VALUES(28,'Plant Power Burger','Crispy plant patty, avocado, lettuce, vegan mayo.',11.94999999999999929,'Burgers','https://images.unsplash.com/photo-1520072959219-c595dc870360?auto=format&fit=crop&w=1200&q=80',1,'2026-01-26 01:21:16.186690');
INSERT INTO menu_items VALUES(29,'Double Cheese Burger','Beef, double cheddar, pickles, ketchup.',13.5,'Burgers','https://images.unsplash.com/photo-1568901346375-23c9450c58cd?auto=format&fit=crop&w=1200&q=80',1,'2026-01-26 01:21:16.186691');
INSERT INTO menu_items VALUES(30,'Skin-on Fries','Crispy fries, sea salt.',3.5,'Sides','https://images.unsplash.com/photo-1541592106381-b31e9677c0e5?auto=format&fit=crop&w=1200&q=80',1,'2026-01-26 01:21:16.186692');
INSERT INTO menu_items VALUES(31,'Loaded Fries (Cheese & Jalapeño)','Cheddar, jalapeño, sauce.',5.950000000000000177,'Sides','https://images.unsplash.com/photo-1541592106381-b31e9677c0e5?auto=format&fit=crop&w=1200&q=80',1,'2026-01-26 01:21:16.186693');
INSERT INTO menu_items VALUES(32,'Garlic Naan','Warm naan brushed with garlic butter.',2.950000000000000177,'Sides','https://images.unsplash.com/photo-1601050690597-df0568f70950?auto=format&fit=crop&w=1200&q=80',1,'2026-01-26 01:21:16.186693');
INSERT INTO menu_items VALUES(33,'Side Salad','Mixed leaves, cucumber, house dressing.',3.950000000000000177,'Sides','https://images.unsplash.com/photo-1512621776951-a57141f2eefd?auto=format&fit=crop&w=1200&q=80',1,'2026-01-26 01:21:16.186694');
INSERT INTO menu_items VALUES(34,'Spiced Corn Ribs','Corn ribs, chilli-lime seasoning.',4.950000000000000177,'Sides','https://images.unsplash.com/photo-1617093727343-374698b1b08d?auto=format&fit=crop&w=1200&q=80',1,'2026-01-26 01:21:16.186695');
INSERT INTO menu_items VALUES(35,'Kids Chicken Bites + Fries','Small portion chicken bites, fries, ketchup.',6.950000000000000177,'Kids Meals','https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?auto=format&fit=crop&w=1200&q=80',1,'2026-01-26 01:21:16.186696');
INSERT INTO menu_items VALUES(36,'Kids Mini Burger + Fries','Mini beef burger, fries, ketchup.',7.5,'Kids Meals','https://images.unsplash.com/photo-1568901346375-23c9450c58cd?auto=format&fit=crop&w=1200&q=80',1,'2026-01-26 01:21:16.186697');
INSERT INTO menu_items VALUES(37,'Kids Veg Nuggets + Fries','Veg nuggets, fries, ketchup.',6.5,'Kids Meals','https://images.unsplash.com/photo-1541592106381-b31e9677c0e5?auto=format&fit=crop&w=1200&q=80',1,'2026-01-26 01:21:16.186698');
INSERT INTO menu_items VALUES(38,'Chocolate Fudge Brownie','Warm brownie, chocolate sauce.',6.5,'Desserts','https://images.unsplash.com/photo-1606313564200-e75d5e30476c?auto=format&fit=crop&w=1200&q=80',1,'2026-01-26 01:21:16.186698');
INSERT INTO menu_items VALUES(39,'Mango Cheesecake','Creamy cheesecake with mango swirl.',6.950000000000000177,'Desserts','https://images.unsplash.com/photo-1542826438-bd32f43d626f?auto=format&fit=crop&w=1200&q=80',1,'2026-01-26 01:21:16.186699');
INSERT INTO menu_items VALUES(40,'Sticky Toffee Pudding','Warm sponge, toffee sauce, cream.',6.950000000000000177,'Desserts','https://images.unsplash.com/photo-1551024601-bec78aea704b?auto=format&fit=crop&w=1200&q=80',1,'2026-01-26 01:21:16.186700');
INSERT INTO menu_items VALUES(41,'Garlic Mayo Dip','Creamy garlic mayo (2oz).',0.75,'Sauces','https://images.unsplash.com/photo-1525351484163-7529414344d8?auto=format&fit=crop&w=1200&q=80',1,'2026-01-26 01:21:16.186701');
INSERT INTO menu_items VALUES(42,'Smoky BBQ Dip','BBQ dip (2oz).',0.75,'Sauces','https://images.unsplash.com/photo-1525351484163-7529414344d8?auto=format&fit=crop&w=1200&q=80',1,'2026-01-26 01:21:16.186702');
INSERT INTO menu_items VALUES(43,'Chilli Honey Dip','Sweet heat dip (2oz).',0.949999999999999956,'Sauces','https://images.unsplash.com/photo-1525351484163-7529414344d8?auto=format&fit=crop&w=1200&q=80',1,'2026-01-26 01:21:16.186703');
INSERT INTO menu_items VALUES(44,'Mint Yoghurt Dip','Cool mint yoghurt (2oz).',0.75,'Sauces','https://images.unsplash.com/photo-1525351484163-7529414344d8?auto=format&fit=crop&w=1200&q=80',1,'2026-01-26 01:21:16.186704');
INSERT INTO menu_items VALUES(45,'Coke (330ml)','Chilled can.',2,'Drinks','https://images.unsplash.com/photo-1544145945-f90425340c7e?auto=format&fit=crop&w=1200&q=80',1,'2026-01-26 01:21:16.186704');
INSERT INTO menu_items VALUES(46,'Sparkling Water','Refreshing and cold.',2.200000000000000178,'Drinks','https://images.unsplash.com/photo-1528825871115-3581a5387919?auto=format&fit=crop&w=1200&q=80',1,'2026-01-26 01:21:16.186705');
INSERT INTO menu_items VALUES(47,'Mango Lassi','Sweet mango yoghurt drink.',3.950000000000000177,'Drinks','https://images.unsplash.com/photo-1528825871115-3581a5387919?auto=format&fit=crop&w=1200&q=80',1,'2026-01-26 01:21:16.186706');
INSERT INTO menu_items VALUES(48,'Fresh Lemonade','Homemade lemonade, mint.',3.5,'Drinks','https://images.unsplash.com/photo-1551024709-8f23befc6f87?auto=format&fit=crop&w=1200&q=80',1,'2026-01-26 01:21:16.186707');
CREATE TABLE orders (
	id INTEGER NOT NULL, 
	user_id INTEGER NOT NULL, 
	order_type VARCHAR(20) NOT NULL, 
	status VARCHAR(30) NOT NULL, 
	total_price NUMERIC(10, 2) NOT NULL, 
	created_at TIMESTAMP NOT NULL, 
	delivery_address_line1 VARCHAR(255), 
	delivery_address_line2 VARCHAR(255), 
	city VARCHAR(80), 
	postcode VARCHAR(20), 
	delivery_instructions TEXT, 
	pickup_time_requested VARCHAR(40), 
	PRIMARY KEY (id), 
	FOREIGN KEY(user_id) REFERENCES users (id)
);
INSERT INTO orders VALUES(1,2,'delivery','delivered',11.68999999999999951,'2026-01-26 01:29:03.794865','904/a Holdenhurst road','','bournemouth','BH88GN','',NULL);
INSERT INTO orders VALUES(2,2,'delivery','delivered',78.84999999999999431,'2026-01-26 01:46:44.426917','904/a Holdenhurst road','','bournemouth','BH88GN','',NULL);
INSERT INTO orders VALUES(3,2,'pickup','delivered',29.23999999999999844,'2026-01-26 02:43:27.719769',NULL,NULL,NULL,NULL,NULL,'18:30');
INSERT INTO orders VALUES(4,2,'delivery','cancelled',34.5,'2026-01-26 04:40:03.372473','58 Cranston Close','','Hounslow','TW33DQ','',NULL);
INSERT INTO orders VALUES(5,2,'delivery','out_for_delivery',39.89999999999999858,'2026-01-26 09:19:32.319161','58 Cranston Close','','Hounslow','TW33DQ','',NULL);
INSERT INTO orders VALUES(6,2,'delivery','pending',26.89999999999999858,'2026-01-26 10:12:36.025472','3 comley road','','Bournemouth','BH92ST','',NULL);
INSERT INTO orders VALUES(7,3,'pickup','pending',17.37999999999999901,'2026-01-26 10:34:56.660286',NULL,NULL,NULL,NULL,NULL,'17:30');
INSERT INTO orders VALUES(8,2,'pickup','pending',53.38000000000000255,'2026-01-27 10:14:36.671537',NULL,NULL,NULL,NULL,NULL,'17:30');
INSERT INTO orders VALUES(9,2,'delivery','pending',56.29999999999999716,'2026-01-27 10:33:15.841628','3 comley road','','Bournemouth','BH92ST','',NULL);
INSERT INTO orders VALUES(10,2,'pickup','pending',32.13000000000000255,'2026-01-27 10:34:44.992970',NULL,NULL,NULL,NULL,NULL,'17:30');
INSERT INTO orders VALUES(11,2,'delivery','pending',31.85000000000000142,'2026-01-27 23:48:43.886092','3 comley road','','Bournemouth','BH92ST','',NULL);
INSERT INTO orders VALUES(12,2,'delivery','pending',15.43999999999999951,'2026-01-27 23:50:28.008487','3 comley road','','Bournemouth','BH92ST','',NULL);
INSERT INTO orders VALUES(13,2,'delivery','pending',18.48999999999999843,'2026-01-27 23:51:19.204842','3 comley road','','Bournemouth','BH92ST','',NULL);
INSERT INTO orders VALUES(14,2,'pickup','pending',10.58000000000000007,'2026-01-28 02:36:14.586632',NULL,NULL,NULL,NULL,NULL,'17:30');
INSERT INTO orders VALUES(15,2,'delivery','pending',20.44000000000000127,'2026-01-28 02:48:25.612482','3 comley road','','Bournemouth','BH92ST','',NULL);
INSERT INTO orders VALUES(16,2,'delivery','pending',16.44000000000000127,'2026-01-28 03:04:41.210413','3 comley road','','Bournemouth','BH92ST','',NULL);
INSERT INTO orders VALUES(17,2,'pickup','delivered',4.209999999999999965,'2026-01-28 03:50:29.876304',NULL,NULL,NULL,NULL,NULL,'17:30');
INSERT INTO orders VALUES(18,2,'delivery','pending',14.89000000000000056,'2026-01-28 04:00:27.302637','3 comley road','','Bournemouth','BH92ST','',NULL);
INSERT INTO orders VALUES(19,2,'pickup','pending',26.69000000000000127,'2026-01-28 05:08:23.398453',NULL,NULL,NULL,NULL,NULL,'17:30');
INSERT INTO orders VALUES(20,2,'delivery','pending',31.39999999999999858,'2026-01-28 05:08:40.580115','3 comley road','','Bournemouth','BH92ST','',NULL);
INSERT INTO orders VALUES(21,2,'delivery','pending',31.39999999999999858,'2026-01-28 05:14:05.461816','3 comley road','','Bournemouth','BH92ST','',NULL);
INSERT INTO orders VALUES(22,2,'pickup','delivered',16.53000000000000113,'2026-01-28 05:26:11.506443',NULL,NULL,NULL,NULL,NULL,'17:30');
INSERT INTO orders VALUES(23,2,'pickup','delivered',6.370000000000000106,'2026-01-28 06:22:04.674184',NULL,NULL,NULL,NULL,NULL,'17:30');
INSERT INTO orders VALUES(24,2,'pickup','delivered',0,'2026-01-28 06:22:25.021384',NULL,NULL,NULL,NULL,NULL,'17:30');
INSERT INTO orders VALUES(25,2,'delivery','delivered',25.83999999999999986,'2026-01-28 06:47:06.900868','3 comley road','','Bournemouth','BH92ST','',NULL);
INSERT INTO orders VALUES(26,3,'delivery','delivered',42.45000000000000285,'2026-01-28 07:01:48.337261','3 comley road','','Bournemouth','BH92ST','',NULL);
INSERT INTO orders VALUES(27,2,'pickup','pending',26.69000000000000127,'2026-01-28 21:55:46.172381',NULL,NULL,NULL,NULL,NULL,'17:30');
INSERT INTO orders VALUES(28,2,'pickup','pending',0,'2026-01-28 22:41:29.537878',NULL,NULL,NULL,NULL,NULL,'17:30');
INSERT INTO orders VALUES(29,2,'delivery','pending',37.89999999999999858,'2026-01-29 05:20:52.033753','3 comley road 345','','Bournemouth','BH92ST','',NULL);
INSERT INTO orders VALUES(30,2,'delivery','pending',35.35000000000000142,'2026-01-29 06:50:04.620407','3 comley road 345','','Bournemouth','BH2 5AA','',NULL);
INSERT INTO orders VALUES(31,2,'delivery','pending',13.93999999999999951,'2026-01-29 07:11:39.419971','3 comley road 345','','Bournemouth','BH23 1AA','',NULL);
INSERT INTO orders VALUES(32,2,'delivery','pending',29,'2026-01-29 08:05:34.809217','3 comley road','','Bournemouth','BH92ST','',NULL);
INSERT INTO orders VALUES(33,2,'delivery','pending',30.44999999999999929,'2026-01-29 08:16:27.352161','3 comley road','','Bournemouth','BH25AA','',NULL);
INSERT INTO orders VALUES(34,2,'delivery','pending',44.45000000000000285,'2026-01-30 03:36:05.086378','3 comley road','','Bournemouth','BH92ST','',NULL);
INSERT INTO orders VALUES(35,3,'delivery','pending',25.39000000000000056,'2026-01-30 07:56:42.331836','3 comley road','','Bournemouth','BH92ST','',NULL);
INSERT INTO orders VALUES(36,3,'delivery','pending',30.44999999999999929,'2026-01-30 08:23:50.395108','3 comley road','','Bournemouth','BH92ST','HI',NULL);
INSERT INTO orders VALUES(37,2,'delivery','pending',39.85000000000000142,'2026-02-01 19:50:43.864859','3 comley road','','Bournemouth','BH92ST','',NULL);
INSERT INTO orders VALUES(38,2,'pickup','pending',19.12000000000000099,'2026-02-01 20:03:39.866489',NULL,NULL,NULL,NULL,NULL,'17:30');
INSERT INTO orders VALUES(39,2,'pickup','pending',19.46000000000000085,'2026-02-01 20:45:49.547148',NULL,NULL,NULL,NULL,NULL,'17:30');
INSERT INTO orders VALUES(40,2,'pickup','pending',38.0799999999999983,'2026-02-02 12:24:06.891196',NULL,NULL,NULL,NULL,NULL,'17:30');
INSERT INTO orders VALUES(41,2,'pickup','out_for_delivery',24.60999999999999944,'2026-02-02 15:11:13.364059',NULL,NULL,NULL,NULL,NULL,'17:30');
CREATE TABLE order_items (
	id INTEGER NOT NULL, 
	order_id INTEGER NOT NULL, 
	menu_item_id INTEGER NOT NULL, 
	quantity INTEGER NOT NULL, 
	unit_price_at_time NUMERIC(10, 2) NOT NULL, 
	line_total NUMERIC(10, 2) NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(order_id) REFERENCES orders (id), 
	FOREIGN KEY(menu_item_id) REFERENCES menu_items (id)
);
INSERT INTO order_items VALUES(1,1,1,1,7.950000000000000177,7.950000000000000177);
INSERT INTO order_items VALUES(2,1,41,1,0.75,0.75);
INSERT INTO order_items VALUES(3,2,5,1,7.5,7.5);
INSERT INTO order_items VALUES(4,2,6,3,19.94999999999999929,59.85000000000000142);
INSERT INTO order_items VALUES(5,2,22,1,11.5,11.5);
INSERT INTO order_items VALUES(6,3,9,1,15.94999999999999929,15.94999999999999929);
INSERT INTO order_items VALUES(7,3,28,1,11.94999999999999929,11.94999999999999929);
INSERT INTO order_items VALUES(8,3,38,1,6.5,6.5);
INSERT INTO order_items VALUES(9,4,10,1,14.5,14.5);
INSERT INTO order_items VALUES(10,4,29,1,13.5,13.5);
INSERT INTO order_items VALUES(11,4,38,1,6.5,6.5);
INSERT INTO order_items VALUES(12,5,4,1,4.950000000000000177,4.950000000000000177);
INSERT INTO order_items VALUES(13,5,10,1,14.5,14.5);
INSERT INTO order_items VALUES(14,5,29,1,13.5,13.5);
INSERT INTO order_items VALUES(15,5,39,1,6.950000000000000177,6.950000000000000177);
INSERT INTO order_items VALUES(16,6,15,1,15.94999999999999929,15.94999999999999929);
INSERT INTO order_items VALUES(17,6,23,1,10.94999999999999928,10.94999999999999928);
INSERT INTO order_items VALUES(18,7,2,1,6.5,6.5);
INSERT INTO order_items VALUES(19,7,17,1,13.94999999999999929,13.94999999999999929);
INSERT INTO order_items VALUES(20,8,18,1,12.94999999999999929,12.94999999999999929);
INSERT INTO order_items VALUES(21,8,23,1,10.94999999999999928,10.94999999999999928);
INSERT INTO order_items VALUES(22,8,28,1,11.94999999999999929,11.94999999999999929);
INSERT INTO order_items VALUES(23,8,29,1,13.5,13.5);
INSERT INTO order_items VALUES(24,8,38,1,6.5,6.5);
INSERT INTO order_items VALUES(25,8,39,1,6.950000000000000177,6.950000000000000177);
INSERT INTO order_items VALUES(26,9,5,1,7.5,7.5);
INSERT INTO order_items VALUES(27,9,11,1,13.94999999999999929,13.94999999999999929);
INSERT INTO order_items VALUES(28,9,14,1,12.94999999999999929,12.94999999999999929);
INSERT INTO order_items VALUES(29,9,18,1,12.94999999999999929,12.94999999999999929);
INSERT INTO order_items VALUES(30,9,39,1,6.950000000000000177,6.950000000000000177);
INSERT INTO order_items VALUES(31,9,45,1,2,2);
INSERT INTO order_items VALUES(32,10,2,1,6.5,6.5);
INSERT INTO order_items VALUES(33,10,31,4,5.950000000000000177,23.80000000000000071);
INSERT INTO order_items VALUES(34,10,36,1,7.5,7.5);
INSERT INTO order_items VALUES(35,11,15,1,15.94999999999999929,15.94999999999999929);
INSERT INTO order_items VALUES(36,11,28,1,11.94999999999999929,11.94999999999999929);
INSERT INTO order_items VALUES(37,11,47,1,3.950000000000000177,3.950000000000000177);
INSERT INTO order_items VALUES(38,12,4,1,4.950000000000000177,4.950000000000000177);
INSERT INTO order_items VALUES(39,12,5,1,7.5,7.5);
INSERT INTO order_items VALUES(40,13,13,1,15.5,15.5);
INSERT INTO order_items VALUES(41,14,4,1,4.950000000000000177,4.950000000000000177);
INSERT INTO order_items VALUES(42,14,5,1,7.5,7.5);
INSERT INTO order_items VALUES(43,15,23,1,10.94999999999999928,10.94999999999999928);
INSERT INTO order_items VALUES(44,15,38,1,6.5,6.5);
INSERT INTO order_items VALUES(45,16,3,1,5.950000000000000177,5.950000000000000177);
INSERT INTO order_items VALUES(46,16,5,1,7.5,7.5);
INSERT INTO order_items VALUES(47,17,4,1,4.950000000000000177,4.950000000000000177);
INSERT INTO order_items VALUES(48,18,4,1,4.950000000000000177,4.950000000000000177);
INSERT INTO order_items VALUES(49,18,39,1,6.950000000000000177,6.950000000000000177);
INSERT INTO order_items VALUES(50,19,4,1,4.950000000000000177,4.950000000000000177);
INSERT INTO order_items VALUES(51,19,7,1,11.94999999999999929,11.94999999999999929);
INSERT INTO order_items VALUES(52,19,10,1,14.5,14.5);
INSERT INTO order_items VALUES(53,20,4,1,4.950000000000000177,4.950000000000000177);
INSERT INTO order_items VALUES(54,20,7,1,11.94999999999999929,11.94999999999999929);
INSERT INTO order_items VALUES(55,20,10,1,14.5,14.5);
INSERT INTO order_items VALUES(56,21,4,1,4.950000000000000177,4.950000000000000177);
INSERT INTO order_items VALUES(57,21,7,1,11.94999999999999929,11.94999999999999929);
INSERT INTO order_items VALUES(58,21,10,1,14.5,14.5);
INSERT INTO order_items VALUES(59,22,5,1,7.5,7.5);
INSERT INTO order_items VALUES(60,22,7,1,11.94999999999999929,11.94999999999999929);
INSERT INTO order_items VALUES(61,23,5,1,7.5,7.5);
INSERT INTO order_items VALUES(62,24,45,1,0,0);
INSERT INTO order_items VALUES(63,25,4,1,4.950000000000000177,4.950000000000000177);
INSERT INTO order_items VALUES(64,25,23,1,10.94999999999999928,10.94999999999999928);
INSERT INTO order_items VALUES(65,25,39,1,6.950000000000000177,6.950000000000000177);
INSERT INTO order_items VALUES(66,26,5,3,7.5,22.5);
INSERT INTO order_items VALUES(67,26,6,1,19.94999999999999929,19.94999999999999929);
INSERT INTO order_items VALUES(68,27,14,1,12.94999999999999929,12.94999999999999929);
INSERT INTO order_items VALUES(69,27,29,1,13.5,13.5);
INSERT INTO order_items VALUES(70,27,34,1,4.950000000000000177,4.950000000000000177);
INSERT INTO order_items VALUES(71,28,45,1,0,0);
INSERT INTO order_items VALUES(72,29,5,1,7.5,7.5);
INSERT INTO order_items VALUES(73,29,12,1,16.94999999999999929,16.94999999999999929);
INSERT INTO order_items VALUES(74,29,38,1,6.5,6.5);
INSERT INTO order_items VALUES(75,29,40,1,6.950000000000000177,6.950000000000000177);
INSERT INTO order_items VALUES(76,30,4,1,4.950000000000000177,4.950000000000000177);
INSERT INTO order_items VALUES(77,30,18,1,12.94999999999999929,12.94999999999999929);
INSERT INTO order_items VALUES(78,30,23,1,10.94999999999999928,10.94999999999999928);
INSERT INTO order_items VALUES(79,30,38,1,6.5,6.5);
INSERT INTO order_items VALUES(80,31,23,1,10.94999999999999928,10.94999999999999928);
INSERT INTO order_items VALUES(81,32,10,2,14.5,29);
INSERT INTO order_items VALUES(82,33,12,1,16.94999999999999929,16.94999999999999929);
INSERT INTO order_items VALUES(83,33,29,1,13.5,13.5);
INSERT INTO order_items VALUES(84,34,10,1,14.5,14.5);
INSERT INTO order_items VALUES(85,34,23,1,10.94999999999999928,10.94999999999999928);
INSERT INTO order_items VALUES(86,34,27,1,12.5,12.5);
INSERT INTO order_items VALUES(87,34,38,1,6.5,6.5);
INSERT INTO order_items VALUES(88,35,5,1,7.5,7.5);
INSERT INTO order_items VALUES(89,35,25,1,9.94999999999999928,9.94999999999999928);
INSERT INTO order_items VALUES(90,35,34,1,4.950000000000000177,4.950000000000000177);
INSERT INTO order_items VALUES(91,36,9,1,15.94999999999999929,15.94999999999999929);
INSERT INTO order_items VALUES(92,36,27,1,12.5,12.5);
INSERT INTO order_items VALUES(93,36,45,1,2,2);
INSERT INTO order_items VALUES(94,37,15,1,15.94999999999999929,15.94999999999999929);
INSERT INTO order_items VALUES(95,37,19,1,13.94999999999999929,13.94999999999999929);
INSERT INTO order_items VALUES(96,37,25,1,9.94999999999999928,9.94999999999999928);
INSERT INTO order_items VALUES(97,38,5,3,7.5,22.5);
INSERT INTO order_items VALUES(98,39,9,1,15.94999999999999929,15.94999999999999929);
INSERT INTO order_items VALUES(99,39,39,1,6.950000000000000177,6.950000000000000177);
INSERT INTO order_items VALUES(100,40,3,1,5.950000000000000177,5.950000000000000177);
INSERT INTO order_items VALUES(101,40,18,3,12.94999999999999929,38.85000000000000142);
INSERT INTO order_items VALUES(102,41,1,1,7.950000000000000177,7.950000000000000177);
INSERT INTO order_items VALUES(103,41,10,1,14.5,14.5);
INSERT INTO order_items VALUES(104,41,38,1,6.5,6.5);
CREATE TABLE loyalty_accounts (
	id INTEGER NOT NULL, 
	user_id INTEGER NOT NULL, 
	points_balance INTEGER NOT NULL, 
	lifetime_earned INTEGER NOT NULL, 
	created_at TIMESTAMP NOT NULL, 
	updated_at TIMESTAMP NOT NULL, lifetime_redeemed INTEGER NOT NULL DEFAULT 0, 
	PRIMARY KEY (id), 
	UNIQUE (user_id), 
	FOREIGN KEY(user_id) REFERENCES users (id)
);
INSERT INTO loyalty_accounts VALUES(1,2,193,1043,'2026-01-28 03:50:07.635363','2026-02-02 15:11:13.387993',850);
INSERT INTO loyalty_accounts VALUES(2,3,97,97,'2026-01-28 07:01:48.367907','2026-01-30 08:23:50.446963',0);
CREATE TABLE loyalty_transactions (
	id INTEGER NOT NULL, 
	user_id INTEGER NOT NULL, 
	order_id INTEGER, 
	kind VARCHAR(32) NOT NULL, 
	points INTEGER NOT NULL, 
	ts TIMESTAMP NOT NULL, 
	note VARCHAR(200), 
	PRIMARY KEY (id), 
	FOREIGN KEY(user_id) REFERENCES users (id), 
	FOREIGN KEY(order_id) REFERENCES orders (id)
);
INSERT INTO loyalty_transactions VALUES(1,2,19,'earn',130,'2026-01-28 05:08:23.424188','Earned from order #19');
INSERT INTO loyalty_transactions VALUES(2,2,20,'earn',155,'2026-01-28 05:08:40.593997','Earned from order #20');
INSERT INTO loyalty_transactions VALUES(3,2,21,'earn',155,'2026-01-28 05:14:05.481836','Earned from order #21');
INSERT INTO loyalty_transactions VALUES(4,2,22,'earn',80,'2026-01-28 05:26:11.525311','Earned from order #22');
INSERT INTO loyalty_transactions VALUES(5,2,NULL,'redeem',400,'2026-01-28 05:26:23.555561','Redeemed: Free Dessert');
INSERT INTO loyalty_transactions VALUES(6,2,23,'earn',30,'2026-01-28 06:22:04.704114','Earned from order #23');
INSERT INTO loyalty_transactions VALUES(7,2,NULL,'redeem',150,'2026-01-28 06:22:10.940897','Redeemed: Free Soft Drink → Coke (330ml)');
INSERT INTO loyalty_transactions VALUES(8,2,24,'earn',10,'2026-01-28 06:22:25.042012','Earned from order #24');
INSERT INTO loyalty_transactions VALUES(9,2,25,'earn',125,'2026-01-28 06:47:06.927309','Earned from order #25');
INSERT INTO loyalty_transactions VALUES(10,3,26,'earn',42,'2026-01-28 07:01:48.374463','Earned from order #26');
INSERT INTO loyalty_transactions VALUES(11,2,27,'earn',26,'2026-01-28 21:55:46.208288','Earned from order #27');
INSERT INTO loyalty_transactions VALUES(12,2,NULL,'redeem',150,'2026-01-28 22:41:16.950706','Redeemed: Free Soft Drink → Coke (330ml)');
INSERT INTO loyalty_transactions VALUES(13,2,28,'earn',5,'2026-01-28 22:41:29.557401','Earned from order #28');
INSERT INTO loyalty_transactions VALUES(14,2,29,'earn',37,'2026-01-29 05:20:52.057867','Earned from order #29');
INSERT INTO loyalty_transactions VALUES(15,2,30,'earn',35,'2026-01-29 06:50:04.644457','Earned from order #30');
INSERT INTO loyalty_transactions VALUES(16,2,31,'earn',13,'2026-01-29 07:11:39.444210','Earned from order #31');
INSERT INTO loyalty_transactions VALUES(17,2,32,'earn',29,'2026-01-29 08:05:34.834262','Earned from order #32');
INSERT INTO loyalty_transactions VALUES(18,2,33,'earn',30,'2026-01-29 08:16:27.372743','Earned from order #33');
INSERT INTO loyalty_transactions VALUES(19,2,34,'earn',44,'2026-01-30 03:36:05.148746','Earned from order #34');
INSERT INTO loyalty_transactions VALUES(20,3,35,'earn',25,'2026-01-30 07:56:42.364498','Earned from order #35');
INSERT INTO loyalty_transactions VALUES(21,3,36,'earn',30,'2026-01-30 08:23:50.452960','Earned from order #36');
INSERT INTO loyalty_transactions VALUES(22,2,37,'earn',39,'2026-02-01 19:50:43.893169','Earned from order #37');
INSERT INTO loyalty_transactions VALUES(23,2,NULL,'redeem',150,'2026-02-01 19:50:55.559456','Redeemed: Free Soft Drink → Coke (330ml)');
INSERT INTO loyalty_transactions VALUES(24,2,38,'earn',19,'2026-02-01 20:03:39.890898','Earned from order #38');
INSERT INTO loyalty_transactions VALUES(25,2,39,'earn',19,'2026-02-01 20:45:49.572154','Earned from order #39');
INSERT INTO loyalty_transactions VALUES(26,2,40,'earn',38,'2026-02-02 12:24:06.915457','Earned from order #40');
INSERT INTO loyalty_transactions VALUES(27,2,41,'earn',24,'2026-02-02 15:11:13.393302','Earned from order #41');
CREATE UNIQUE INDEX ix_users_email ON users (email);
CREATE INDEX ix_menu_items_category ON menu_items (category);
CREATE INDEX ix_orders_user_id ON orders (user_id);
CREATE INDEX ix_order_items_menu_item_id ON order_items (menu_item_id);
CREATE INDEX ix_order_items_order_id ON order_items (order_id);
