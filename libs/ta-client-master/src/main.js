import Datafeed from "./datafeed.js";
import { makeApiRequest } from "./helper.js";
import { getLastsActiveThresh } from "./utils/divergence.js";

if (Notification["permission"] === "granted") {
  localStorage.setItem("notifPermision", true);
} else if (Notification["permission"] !== "denied") {
  Notification.requestPermission().then((per) => {
    const isPermision = per === "denied" ? false : true;
    localStorage.setItem("notifPermision", isPermision);
  });
}

// Build The Cahrt
(async () => {
  const res = await makeApiRequest("/widgetConf");
  const { tf, exchange, symbol } = res;

  window.tvWidget = new TradingView.widget({
    symbol: `${exchange}:${symbol}` || "unknown",
    datafeed: Datafeed, // our datafeed object
    interval: tf || 5,
    container_id: "tv_chart_container",
    locale: "en",
    enabled_features: [],
    client_id: "test",
    user_id: "public_user_id",
    fullscreen: true,
    autosize: true,
    overrides: {
      "paneProperties.background": "#131722",
      "paneProperties.vertGridProperties.color": "#363c4e",
      "paneProperties.horzGridProperties.color": "#363c4e",
      "symbolWatermarkProperties.transparency": 90,
      "scalesProperties.textColor": "#AAA",
      "mainSeriesProperties.candleStyle.wickUpColor": "#336854",
      "mainSeriesProperties.candleStyle.wickDownColor": "#7f323f",
    },
    library_path: "../charting_library/charting_library/",
    debug: false,
  });

  // window.tvWidget.onChartReady(function () {
  //   widget.chart().createStudy("MACD", false, true);
  // });

  // Chaeck active Strategies
  const divergence = await makeApiRequest("/divergence");
  const { zigzagThreshs, data: dvgData } = divergence;
  Array.isArray(dvgData) &&
    dvgData.map((data) => getLastsActiveThresh(zigzagThreshs, data));
})();
