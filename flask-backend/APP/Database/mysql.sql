CREATE TABLE User
(
  Name VARCHAR(255) NOT NULL,
  Email_Id VARCHAR(255) NOT NULL,
  PRIMARY KEY (Email_Id)
);

CREATE TABLE LoginDetails
(
  Password VARCHAR(255) NOT NULL,
  Email_Id VARCHAR(255) NOT NULL,
  PRIMARY KEY (Email_Id),
  FOREIGN KEY (Email_Id) REFERENCES User(Email_Id) ON DELETE CASCADE
);

CREATE TABLE Item
(
  Item_Id INTEGER PRIMARY KEY  AUTOINCREMENT,
  Name VARCHAR(255) NOT NULL,
  Description VARCHAR(255),
  Email_Id VARCHAR(255) NOT NULL,
  FOREIGN KEY (Email_Id) REFERENCES User(Email_Id) ON DELETE CASCADE
);

CREATE TABLE SaleAdvertisement
(
  Date DATE NOT NULL,
  AdvertisementId INTEGER PRIMARY KEY  AUTOINCREMENT,
  Cost INT NOT NULL,
  Item_Id INT NOT NULL,
  FOREIGN KEY (Item_Id) REFERENCES Item(Item_Id) ON DELETE CASCADE
);

CREATE TABLE Transactions
(
  Transaction_ID INTEGER PRIMARY KEY  AUTOINCREMENT,
  Cost INT NOT NULL,
  Date DATE NOT NULL,
  Item_Id INT NOT NULL,
  BuyerEmail_Id VARCHAR(255) NOT NULL,
  SellerEmail_Id VARCHAR(255) NOT NULL,
  FOREIGN KEY (Item_Id) REFERENCES Item(Item_Id) ON DELETE CASCADE,
  FOREIGN KEY (BuyerEmail_Id) REFERENCES User(Email_Id) ON DELETE CASCADE,
  FOREIGN KEY (SellerEmail_Id) REFERENCES User(Email_Id) ON DELETE CASCADE
);

CREATE TABLE Reviews
(
  Rating INT NOT NULL,
  Review VARCHAR(255) NOT NULL,
  ReviewId INTEGER PRIMARY KEY  AUTOINCREMENT,
  Date DATE NOT NULL,
  Email_Id VARCHAR(255) NOT NULL,
  Item_Id INT NOT NULL,
  FOREIGN KEY (Email_Id) REFERENCES User(Email_Id) ON DELETE CASCADE,
  FOREIGN KEY (Item_Id) REFERENCES Item(Item_Id) ON DELETE CASCADE
);

CREATE TABLE Wishlist
(
  Email_Id VARCHAR(255) NOT NULL,
  Item_Id INT NOT NULL,
  PRIMARY KEY (Email_Id, Item_Id),
  FOREIGN KEY (Email_Id) REFERENCES User(Email_Id) ON DELETE CASCADE,
  FOREIGN KEY (Item_Id) REFERENCES Item(Item_Id) ON DELETE CASCADE
);

CREATE TABLE User_Mobile_Number
(
  Mobile_Number VARCHAR(255) NOT NULL,
  Email_Id VARCHAR(255) NOT NULL,
  PRIMARY KEY (Mobile_Number, Email_Id),
  FOREIGN KEY (Email_Id) REFERENCES User(Email_Id) ON DELETE CASCADE
);

-- TODO UPDATE THIS IN ERD
CREATE TABLE Item_Image
(
  ImageId INTEGER PRIMARY KEY  AUTOINCREMENT,
  Image  BLOB NOT NULL,
  Item_Id INT NOT NULL,
  FOREIGN KEY (Item_Id) REFERENCES Item(Item_Id) ON DELETE CASCADE
);

CREATE TABLE Address
(
  House_No VARCHAR(255) NOT NULL,
  Street VARCHAR(255) NOT NULL,
  City VARCHAR(255) NOT NULL,
  Country VARCHAR(255) NOT NULL,
  PinCode INT NOT NULL,
  Email_Id VARCHAR(255) NOT NULL,
  PRIMARY KEY (House_No, Street, City, Country, PinCode, Email_Id),
  FOREIGN KEY (Email_Id) REFERENCES User(Email_Id) ON DELETE CASCADE
);