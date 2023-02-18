export const sleep = async (sec: number) => await new Promise((resolve) => setTimeout(resolve, sec));
