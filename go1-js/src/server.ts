import express from "express";
import { Go1, Go1Mode } from "./go1";

const router = express.Router();

const walkingTime = 100;
const turningTime = 600;
const dog = new Go1();
dog.init();

router.get("/forward", (req, res) => {
  dog.setMode(Go1Mode.walk);
  dog.goForward(0.25, 100);

  res.send("Forward");
});
router.get("/forward-long", (req, res) => {
  dog.setMode(Go1Mode.walk);
  dog.goForward(0.25, walkingTime * 3);

  res.send("Forward");
});

router.get("/backward", (req, res) => {
  dog.setMode(Go1Mode.walk);
  dog.goBackward(0.25, walkingTime);

  res.send("Backward");
});

router.get("/left", (req, res) => {
  dog.setMode(Go1Mode.walk);
  dog.turnLeft(0.25, turningTime);

  res.send("Left");
});

router.get("/right", (req, res) => {
  dog.setMode(Go1Mode.walk);
  dog.turnRight(0.25, turningTime);

  res.send("Right");
});
router.get("/dance", (req, res) => {
  dog.setMode(Go1Mode.dance1);

  res.send("dance");
});

// run server
const app = express();
app.use("/api", router);

app.listen(process.env.PORT || 3012, () => {
  console.log("Server running on port 3012");
});
