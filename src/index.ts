import { pad3 } from "./../module/pad3";
import { sleep } from "./../module/sleep";
import { resetQuery, writeQuery } from "../module/fs";
import { ResponseType } from "./index.d";
/* NodeJs 12 샘플 코드 */
// DataSet: https://www.data.go.kr/data/15057639/openapi.do
// 또는
// https://www.data.go.kr/tcs/dss/selectApiDataDetailView.do?publicDataPk=15057639

import * as dotenv from "dotenv";
dotenv.config();
import axios from "axios";
import SqlString from "sqlstring";

const key = process.env.SERVICE_KEY;
if (!key) console.log("서비스 키를 찾을 수 없습니다.");

const f = async (page: number) => {
  const url = `http://apis.data.go.kr/1471000/MdcinGrnIdntfcInfoService01/getMdcinGrnIdntfcInfoList01?serviceKey=${key}&numOfRows=300&type=json&pageNo=${page}`;
  await axios
    .get(url)
    .then((d) => d.data)
    .then((d: ResponseType) => {
      const data = d.body ? d.body.items : null;
      if (!data) return;
      data.map(async (item, index) => {
        const sql = SqlString.format("INSERT INTO medicine SET ?", { ...item, page, index });
        await writeQuery(`${sql};\n`);
      });
    })
    .catch((err) => console.log("ERROR:", err));
};

const start = async () => {
  const max = 100;
  for (let i = 1; i <= max; i++) {
    console.log(`[${pad3(i)}/${pad3(max)}] start ~`);
    await f(i);
    sleep(200);
    console.log(`[${pad3(i)}/${pad3(max)}] completed ~ !`);
  }
};

resetQuery();
start();
