export const getLastsActiveThresh = (threshNum, dvgData) => {
  // console.log(dvgData);
  const { name, description, stoch, macd, rsi } = dvgData;
  //   console.log(stoch.findLast((elm)=> elm === true) || "not ")
  //   console.log(rsi.findLast((elm)=> elm === true) || "not ")
  // let toShow = [];

  let macdIdx = threshNum[getLastElementIdx(macd)];
  let rsiIdx = threshNum[getLastElementIdx(rsi)];
  let stochIdx = threshNum[getLastElementIdx(stoch)];

  addActiveLinks("Macd", description, macdIdx, "macd");
  // addActiveLinks("RSI", description, rsiIdx, "rsi");
  // addActiveLinks("Stoch", description, stochIdx, "stoch");

  // toShow.push({
  //   Strategy: "macd " + description,

  //   ActiveZigZagNUmber: threshNum[macdIdx],
  // });

  // const mcdE = document.createElement("a");
  // mcdE.innerHTML = `Macd ${description} | Active ZigZag NUmber : ${threshNum[macdIdx]}`;
  // mcdE.href = "sd";

  // toShow.push({
  //   Strategy: "rsi " + description,

  //   ActiveZigZagNUmber: threshNum[rsiIdx],
  // });
  // toShow.push({
  //   Strategy: "stoch " + description,
  //   ActiveZigZagNUmber: threshNum[stochIdx],
  // });

  // x = ``
};

const getLastElementIdx = (strategy) => {
  let idx;

  strategy.findLast((el, i) => {
    if (el) {
      idx = i;
    }
  });

  return idx;
};

export const addActiveLinks = (name, desc, number, href) => {
  const element = document.createElement("a");
  const br = document.createElement("hr");
  element.innerHTML = `${name} ${desc} | Active ZigZag NUmber : ${number || 0.2}`;
  element.href = href;
  document.getElementById("active_list").appendChild(element);
  document.getElementById("active_list").appendChild(br);
};
