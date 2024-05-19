import express from "express";
import { Go1, Go1Mode } from "./go1";

const router = express.Router();

router.get("/forward", (req, res) => {
  const dog = new Go1();
  dog.init();
  dog.setMode(Go1Mode.walk);
  dog.goForward(0.25, 200);

  res.send("Forward");
});

router.get("/backward", () => {
  const dog = new Go1();
  dog.init();
  dog.setMode(Go1Mode.walk);
  dog.goBackward(0.25, 200);
});

router.get("/left", () => {
  const dog = new Go1();
  dog.init();
  dog.setMode(Go1Mode.walk);
  dog.turnLeft(0.25, 200);
});

router.get("/right", () => {
  const dog = new Go1();
  dog.init();
  dog.setMode(Go1Mode.walk);
  dog.turnRight(0.25, 200);
});

// run server
const app = express();
app.use("/api", router);

app.listen(process.env.PORT || 3012, () => {
  console.log("Server running on port 3012");
});
