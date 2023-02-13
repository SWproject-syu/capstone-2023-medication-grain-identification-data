import fs from "fs";
export const writeQuery = async (content: string) => await fs.writeFileSync("./out/query.txt", content, { flag: "a+" });
export const resetQuery = async () => fs.writeFile("./out/query.txt", "", "utf8", () => {});
