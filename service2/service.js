import express from "express";
import { statfs } from "fs/promises";
import fs from "fs"

const app = express();

const STORAGE_URL  = process.env.STORAGE_URL;
const VSTORAGE     = process.env.VSTORAGE_PATH;
const PORT         = process.env.PORT;

const UP = Date.now();
const now = () => new Date().toISOString().slice(0, 19) + "Z";;
const uptimeHours = () => (Date.now() - UP) / (1000 * 60 * 60);

export async function free() {
    const fsStats = await statfs("/");
    const bytes = fsStats.bsize * fsStats.bavail;
    return bytes / (1024 * 1024);
};

const createRecord = async () => {
    const space = await free();
    return `Timestamp2: ${now()}: uptime ${uptimeHours().toFixed(2)} hours, free disk in root: ${space.toFixed(1)} MBytes`;
};

app.get("/status", async (request, response) => {
    const record = await  createRecord();
    await fetch(`${STORAGE_URL}/log`, { method: "POST", headers: { "Content-Type": "text/plain" }, body: record });
    fs.appendFileSync(VSTORAGE, record + "\n");
    response.type("text/plain").send(record);
});


app.listen(PORT, "0.0.0.0");

console.log(`Service 2 running on port ${PORT}`)