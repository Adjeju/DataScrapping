require("dotenv").config();
const mongoose = require("mongoose");
const express = require("express");
const User = require("./models/userModel");
const Item = require("./models/itemModel");
const bcrypt = require("bcryptjs");
const jwt = require("jsonwebtoken");
const app = express();
const PORT = 3000;

app.use(express.json());

app.post("/register", async (req, res) => {
  try {
    const { login, email, password } = req.body;

    if (!(email && password && login)) {
      res.status(400).send("All input is required");
    }

    const oldUser = await User.findOne({ login });

    if (oldUser) {
      return res.status(409).send("User Already Exist. Please Login");
    }

    encryptedPassword = await bcrypt.hash(password, 10);

    const user = await User.create({
      login,
      email: email.toLowerCase(),
      password: encryptedPassword,
    });

    const token = jwt.sign(
      { user_id: user._id, email },
      process.env.TOKEN_KEY,
      {
        expiresIn: "2h",
      }
    );
    user.token = token;

    res.status(201).json(user);
  } catch (err) {
    console.log(err);
  }
});

app.post("/login", async (req, res) => {
  try {
    const { login, password } = req.body;
    if (!(login && password)) {
      res.status(400).send("All input is required");
    }
    const user = await User.findOne({ login });
    if (user && (await bcrypt.compare(password, user.password))) {
      const token = jwt.sign(
        { user_id: user._id, login },
        process.env.TOKEN_KEY,
        {
          expiresIn: "2h",
        }
      );
      user.token = token;
      res.status(200).json(user);
    }
  } catch (err) {
    console.log(err);
  }
});

app.post("/item", async (req, res) => {
  try {
    const { model, price, link, image_url } = req.body;
    if (!(model && price && link && image_url)) {
      res.status(400).send("All input is required");
    }
    const item = await Item.create({
      model,
      price,
      link,
      image_url,
    });

    res.status(201).json(item);
  } catch (error) {
    res.sendStatus(404);
  }
});

app.put("/item", async (req, res) => {
  try {
    const { model, price } = req.body;
    const item = await Item.findOneAndUpdate(
      {
        model,
        price,
      },
      req.body
    );

    res.status(201).json(item);
  } catch (error) {
    res.sendStatus(404);
  }
});

app.get("/items", async (req, res) => {
  try {
    if (!req.query.name && req.query.price) {
      const items = await Item.find();
      res.send(items);
    }
    const { name, price } = req.query;
    const item = await Item.findOne({ name, price });
    console.log(name, price);
    console.log(item);
    if (item) {
      res.send(item);
    } else {
      res.sendStatus(404);
    }
  } catch (error) {
    return res.sendStatus(404);
  }
});

main();

async function main() {
  await mongoose.connect(process.env.MONGO_URI);
}

app.listen(PORT, () => {
  console.log(`Example app listening on port ${PORT}`);
});
