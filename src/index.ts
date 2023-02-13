import { resetQuery, writeQuery } from "../module/fs";
import { ResponseType } from "./index.d";
/* NodeJs 12 샘플 코드 */
// DataSet: https://www.data.go.kr/data/15057639/openapi.do
// 또는
// https://www.data.go.kr/tcs/dss/selectApiDataDetailView.do?publicDataPk=15057639

import * as dotenv from "dotenv";
dotenv.config();
import axios from "axios";
const key = process.env.SERVICE_KEY;
if (!key) console.log("서비스 키를 찾을 수 없습니다.");

const url = "http://apis.data.go.kr/1471000/MdcinGrnIdntfcInfoService01/getMdcinGrnIdntfcInfoList01";
let queryParams = "?" + encodeURIComponent("serviceKey") + `=${key}`; /* Service Key*/
// queryParams += "&" + encodeURIComponent("item_name") + "=" + encodeURIComponent(""); /* */
// queryParams += "&" + encodeURIComponent("entp_name") + "=" + encodeURIComponent(""); /* */
// queryParams += "&" + encodeURIComponent("item_seq") + "=" + encodeURIComponent(""); /* */
// queryParams += "&" + encodeURIComponent("img_regist_ts") + "=" + encodeURIComponent(""); /* */
// queryParams += "&" + encodeURIComponent("pageNo") + "=" + encodeURIComponent("1"); /* */
queryParams += "&" + encodeURIComponent("numOfRows") + "=" + encodeURIComponent("300"); /* */
// queryParams += "&" + encodeURIComponent("edi_code") + "=" + encodeURIComponent(""); /* */
queryParams += "&" + encodeURIComponent("type") + "=" + encodeURIComponent("json"); /* */

axios
  .get(`${url}${queryParams}`)
  .then((d) => d.data)
  .then((d: ResponseType) => {
    resetQuery();
    d.body.items.map(async (item) => {
      await writeQuery(`INSERT INTO medicine ${item.CHART}\n`);
    });
  })
  .catch((err) => console.log("ERROR:", err));

// (error, response, body) => {
//   //console.log('Status', response.statusCode);
//   //console.log('Headers', JSON.stringify(response.headers));
//   //console.log('Reponse received', body);
// };
