
chrome.tabs.onUpdated.addListener(function(tabId, changeInfo, tab) {
    if (changeInfo.status == 'complete') {
        if (tab.url.endsWith('/cart') && tab.url.startsWith('https://www.selver.ee/')) {
            chrome.tabs.sendMessage(tabId, {page: "cart"});
        } else if (tab.url.includes("search") && tab.url.startsWith('https://www.selver.ee/')) {
            chrome.tabs.sendMessage(tabId, {page: "search"});
        } else if (tab.url.startsWith('https://www.selver.ee/')) {
            chrome.tabs.sendMessage(tabId, {page: "product"});
        };
    }
});
