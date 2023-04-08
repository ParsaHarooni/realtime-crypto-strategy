import { configurationData, API_URL } from "./config.js";
// Make requests to the server
export async function makeApiRequest(path, apiURL = API_URL) {
  try {
    const address = `${apiURL}${path}`;
    const response = await fetch(address);
    return response.json();
  } catch (error) {
    throw new Error(`request error: ${error}`);
  }
}

// Generate a symbol ID from a pair of the coins
export function generateSymbol(exchange, fromSymbol, toSymbol) {
  const short = `${fromSymbol}/${toSymbol}`;
  return {
    short,
    full: `${exchange}:${short}`,
  };
}

const getAllSymbols = async () => {
  const data = await makeApiRequest("/exchanges");
  let allSymbols = [];

  for (const exchange of configurationData.exchanges) {
    const pairs = data.Data[exchange.value].pairs;

    for (const leftPairPart of Object.keys(pairs)) {
      const symbols = pairs[leftPairPart].map((rightPairPart) => {
        const symbol = generateSymbol(
          exchange.value,
          leftPairPart,
          rightPairPart
        );
        return {
          symbol: symbol.short,
          full_name: symbol.full,
          description: symbol.short,
          exchange: exchange.value,
          type: "crypto",
        };
      });
      allSymbols = [...allSymbols, ...symbols];
    }
  }
  return allSymbols;
};

// load all symbols for all supported exchanges
export const toResolveSymbol = async (
  symbolName,
  onSymbolResolvedCallback,
  onResolveErrorCallback,
  extension
) => {
  console.log("[resolveSymbol]: Method call", symbolName);
  const symbols = await getAllSymbols();
  const symbolItem = symbols.find(({ full_name }) => full_name === symbolName);
  if (!symbolItem) {
    console.log("[resolveSymbol]: Cannot resolve symbol", symbolName);
    onResolveErrorCallback("cannot resolve symbol");
    return;
  }
  const symbolInfo = {
    ticker: symbolItem.full_name,
    name: symbolItem.symbol,
    description: symbolItem.description,
    type: symbolItem.type,
    session: "24x7",
    timezone: "Etc/UTC",
    exchange: symbolItem.exchange,
    minmov: 1,
    pricescale: 100,
    has_intraday: false,
    has_no_volume: true,
    has_weekly_and_monthly: false,
    supported_resolutions: configurationData.supported_resolutions,
    volume_precision: 2,
    data_status: "streaming",
  };

  console.log("[resolveSymbol]: Symbol resolved", symbolName);
  // strategy notif
  // if ("Notification" in window && Notification.permission === "granted")
  // new Notification("Symbol resolved", {
  //   body: symbolName,
  // });
  onSymbolResolvedCallback(symbolInfo);
};

export function parseFullSymbol(fullSymbol) {
  const match = fullSymbol.match(/^(\w+):(\w+)\/(\w+)$/);
  if (!match) {
    return null;
  }

  return { exchange: match[1], fromSymbol: match[2], toSymbol: match[3] };
}

export const toGetBars = async (
  symbolInfo,
  resolution,
  periodParams,
  onHistoryCallback,
  onErrorCallback
) => {
  const { from, to, firstDataRequest } = periodParams;
  console.log("[getBars]: Method call", symbolInfo, resolution, from, to);
  const parsedSymbol = parseFullSymbol(symbolInfo.full_name);
  const urlParameters = {
    e: parsedSymbol.exchange,
    fsym: parsedSymbol.fromSymbol,
    tsym: parsedSymbol.toSymbol,
    toTs: to,
    limit: 2000,
  };
  const query = Object.keys(urlParameters)
    .map((name) => `${name}=${encodeURIComponent(urlParameters[name])}`)
    .join("&");
  try {
    // const data = await makeApiRequest(`data/histoday?${query}`);
    const data = await makeApiRequest("/ohlcv");
    console.log(data);
    // if (
    //   (data.Response && data.Response === "Error") ||
    //   data.Data.length === 0
    // ) {
    //   // "noData" should be set if there is no data in the requested period.
    //   onHistoryCallback([], { noData: true });
    //   return;
    // }
    let bars = [];
    // data.Data.forEach((bar) => {
    //   if (bar.time >= from && bar.time < to) {
    //     bars = [
    //       ...bars,
    //       {
    //         time: bar.time * 1000,
    //         low: bar.low,
    //         high: bar.high,
    //         open: bar.open,
    //         close: bar.close,
    //       },
    //     ];
    //   }
    // });
    data.data.forEach((bar) => {
      // ['Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']
      let [time, open, high, low, close] = bar;

      let iso = new Date(time);
      time = iso.getTime();

      // if (time >= from && time < to) {
      bars = [
        ...bars,
        {
          time: time,
          low: low,
          high: high,
          open: open,
          close: close,
        },
      ];
      // }
    });

    console.log(`[getBars]: returned ${bars.length} bar(s)`);
    onHistoryCallback(bars, { noData: false });
  } catch (error) {
    console.log("[getBars]: Get error", error);
    onErrorCallback(error);
  }
};

export const toSearchSymbol = async (
  userInput,
  exchange,
  symbolType,
  onResultReadyCallback
) => {
  console.log("[searchSymbols]: Method call");
  const symbols = await getAllSymbols();
  const newSymbols = symbols.filter((symbol) => {
    const isExchangeValid = exchange === "" || symbol.exchange === exchange;
    const isFullSymbolContainsInput =
      symbol.full_name.toLowerCase().indexOf(userInput.toLowerCase()) !== -1;
    return isExchangeValid && isFullSymbolContainsInput;
  });
  onResultReadyCallback(newSymbols);
};
