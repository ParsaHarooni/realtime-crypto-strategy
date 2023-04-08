import { toResolveSymbol, toGetBars, toSearchSymbol } from "./helper.js";
import { configurationData } from "./config.js";

import { subscribeOnStream, unsubscribeFromStream } from "./streaming.js";

export default {
  onReady: (callback) => {
    console.log("[onReady]: Method call");
    setInterval(() => callback(configurationData));
  },
  searchSymbols: toSearchSymbol,
  resolveSymbol: toResolveSymbol,
  getBars: toGetBars,
  subscribeBars: (
    symbolInfo,
    resolution,
    onRealtimeCallback,
    subscriberUID,
    onResetCacheNeededCallback
  ) => {
    console.log(
      "[subscribeBars]: Method call with subscriberUID:",
      subscriberUID
    );
    // strategy notif
    // if ("Notification" in window && Notification.permission === "granted")
    //   new Notification("Method call", {
    //     body: subscriberUID,
    //   });
    subscribeOnStream(
      symbolInfo,
      resolution,
      onRealtimeCallback,
      subscriberUID,
      onResetCacheNeededCallback,
      lastBarsCache.get(symbolInfo.full_name)
    );
  },
  unsubscribeBars: (subscriberUID) => {
    console.log(
      "[unsubscribeBars]: Method call with subscriberUID:",
      subscriberUID
    );
    unsubscribeFromStream(subscriberUID);
  },
};
