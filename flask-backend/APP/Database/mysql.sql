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
  FOREIGN KEY (Email_Id) REFERENCES User(Email_Id)
);

CREATE TABLE Item
(
  Item_Id INT NOT NULL,
  Name VARCHAR(255) NOT NULL,
  Description VARCHAR(255),
  Email_Id VARCHAR(255) NOT NULL,
  PRIMARY KEY (Item_Id),
  FOREIGN KEY (Email_Id) REFERENCES User(Email_Id)
);

CREATE TABLE SaleAdvertisement
(
  Date DATE NOT NULL,
  AdvertisementId INT NOT NULL,
  Cost INT NOT NULL,
  Item_Id INT NOT NULL,
  PRIMARY KEY (AdvertisementId),
  FOREIGN KEY (Item_Id) REFERENCES Item(Item_Id)
);

CREATE TABLE Transactions
(
  Transaction_ID INT NOT NULL,
  Cost INT NOT NULL,
  Date DATE NOT NULL,
  Item_Id INT NOT NULL,
  BuyerEmail_Id VARCHAR(255) NOT NULL,
  SellerEmail_Id VARCHAR(255) NOT NULL,
  PRIMARY KEY (Transaction_ID),
  FOREIGN KEY (Item_Id) REFERENCES Item(Item_Id),
  FOREIGN KEY (BuyerEmail_Id) REFERENCES User(Email_Id),
  FOREIGN KEY (SellerEmail_Id) REFERENCES User(Email_Id)
);

CREATE TABLE Reviews
(
  Rating INT NOT NULL,
  Review VARCHAR(255) NOT NULL,
  ReviewId INT NOT NULL,
  Date DATE NOT NULL,
  Email_Id VARCHAR(255) NOT NULL,
  Item_Id INT NOT NULL,
  PRIMARY KEY (ReviewId),
  FOREIGN KEY (Email_Id) REFERENCES User(Email_Id),
  FOREIGN KEY (Item_Id) REFERENCES Item(Item_Id)
);

CREATE TABLE Wishlist
(
  Email_Id VARCHAR(255) NOT NULL,
  Item_Id INT NOT NULL,
  PRIMARY KEY (Email_Id, Item_Id),
  FOREIGN KEY (Email_Id) REFERENCES User(Email_Id),
  FOREIGN KEY (Item_Id) REFERENCES Item(Item_Id)
);

CREATE TABLE User_Mobile_Number
(
  Mobile_Number VARCHAR(255) NOT NULL,
  Email_Id VARCHAR(255) NOT NULL,
  PRIMARY KEY (Mobile_Number, Email_Id),
  FOREIGN KEY (Email_Id) REFERENCES User(Email_Id)
);

CREATE TABLE Item_Image
(
  ImageId INT NOT NULL,
  Image  BLOB NOT NULL,
  Item_Id INT NOT NULL,
  PRIMARY KEY (ImageId, Item_Id),
  FOREIGN KEY (Item_Id) REFERENCES Item(Item_Id)
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
  FOREIGN KEY (Email_Id) REFERENCES User(Email_Id)
);