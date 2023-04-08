import { parseFullSymbol } from './helper.js';

const channelToSubscription = new Map();

const socket = io('wss://streamer.cryptocompare.com');

socket.on('connect', () => {
    console.log('[socket] Connected');
});

socket.on('disconnect', (reason) => {
    console.log('[socket] Disconnected:', reason);
});

socket.on('error', (error) => {
    console.log('[socket] Error:', error);
});

export function subscribeOnStream(
    symbolInfo,
    resolution,
    onRealtimeCallback,
    subscriberUID,
    onResetCacheNeededCallback,
    lastDailyBar
) {
    const parsedSymbol = parseFullSymbol(symbolInfo.full_name);
    const channelString = `0~${parsedSymbol.exchange}~${parsedSymbol.fromSymbol}~${parsedSymbol.toSymbol}`;
    const handler = {
        id: subscriberUID,
        callback: onRealtimeCallback,
    };
    let subscriptionItem = channelToSubscription.get(channelString);
    if (subscriptionItem) {
        // already subscribed to the channel, use the existing subscription
        subscriptionItem.handlers.push(handler);
        return;
    }
    subscriptionItem = {
        subscriberUID,
        resolution,
        lastDailyBar,
        handlers: [handler],
    };
    channelToSubscription.set(channelString, subscriptionItem);
    console.log('[subscribeBars]: Subscribe to streaming. Channel:', channelString);
    socket.emit('SubAdd', { subs: [channelString] });
}

export function unsubscribeFromStream(subscriberUID) {

    // find a subscription with id === subscriberUID
    for (const channelString of channelToSubscription.keys()) {
        const subscriptionItem = channelToSubscription.get(channelString);
        const handlerIndex = subscriptionItem.handlers
            .findIndex(handler => handler.id === subscriberUID);

        if (handlerIndex !== -1) {
            // remove from handlers
            subscriptionItem.handlers.splice(handlerIndex, 1);

            if (subscriptionItem.handlers.length === 0) {
                // unsubscribe from the channel, if it was the last handler
                console.log('[unsubscribeBars]: Unsubscribe from streaming. Channel:', channelString);
                socket.emit('SubRemove', { subs: [channelString] });
                channelToSubscription.delete(channelString);
                break;
            }
        }
    }
}