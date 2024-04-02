import express from "express"
import multer from "multer"
import { spawn } from "child_process"

const storage = multer.diskStorage({
    destination: "uploads/",

    filename: function(req, file, cb){
        cb(null, file.originalname)
    }
})
const upload = multer({ storage: storage })
const app = express()
const port = 3000

app.use(express.static("public"))

const executePython = async (script, replay) => {
    return new Promise((resolve, reject) => {
        const py = spawn('python3', [script, replay]);
        let output = '';
        py.stdout.on('data', (data) => {
            output += data.toString(); // Append data to output
        });
        py.stderr.on('data', (data) => {
            console.error(`Error: ${data}`);
            reject(`Error occurred in ${script}`);
        });
        py.on('close', (code) => {
            console.log(`Script was executed with code: ${code}`);
            resolve(output);
        });
    });
};

const standardStats = {
    Minimum_BPM: 375,
    Maximum_BPM: 475,
    Maximum_Boost_Used_While_Supersonic: 250,
    Minimum_Big_Boost_Pads: 18,
    Maximum_Big_Boost_Pads: 26,
    Minumum_Small_Boost_Pads: 65,
    Percentage_on_Defensive_Half: 60.0,
    Percentage_on_Offensive_Half: 40.0,
    Minum_Speed: 1550,
    Maximum_Speed: 1650
}

app.get("/", (req, res) => {
    res.render("home.ejs")
})

app.post("/submit", upload.single("replay_file"), async (req, res) => {
    const fileName = req.file.filename
    let userData = await executePython('/Users/doc/Desktop/Full-Stack/rl_helper/stats.py', `/Users/doc/Desktop/Full-Stack/rl_helper/uploads/${fileName}`)
    // make userData a list here
    
    userData = userData.replaceAll("'", '"').replaceAll("True", true).replaceAll("False", false)
    const userDataJson = JSON.parse(userData)
    let playerData = userDataJson.slice(1)
    let gameData = userDataJson.slice(0,1)
    gameData = gameData[0]
    app.set("filePlayerData", playerData)
    app.set("fileGameData", gameData)
    res.redirect("/compare")
})

app.get("/compare", (req, res) => {
    const fileGameData = app.get('fileGameData')
    const filePlayerData = app.get('filePlayerData')
    res.render('compare.ejs', {playerData: filePlayerData, gameData: fileGameData, expectedData: standardStats})
})

app.listen(port, () => {
    console.log(`Listening on port: ${port}`)
})
