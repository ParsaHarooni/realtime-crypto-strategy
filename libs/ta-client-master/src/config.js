export const API_URL = "http://127.0.0.1:5000";

export const configurationData = {
  supported_resolutions: ["5","10","15","60","1D", "1W", "1M"],
  exchanges: [
    {
      value: "Bitfinex",
      name: "Bitfinex",
      desc: "Bitfinex",
    },
    {
      // `exchange` argument for the `searchSymbols` method, if a user selects this exchange
      value: "Kraken",

      // filter name
      name: "Kraken",

      // full exchange name displayed in the filter popup
      desc: "Kraken bitcoin exchange",
    },
  ],
  symbols_types: [
    {
      name: "crypto",

      // `symbolType` argument for the `searchSymbols` method, if a user selects this symbol type
      value: "crypto",
    },
    // ...
  ],
};
