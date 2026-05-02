/**
 * GitScope AI - Background Service Worker
 * Handles side panel opening and message routing
 */

const API_BASE = "http://localhost:8000/api";

// Open side panel when action icon is clicked
chrome.action.onClicked.addListener((tab) => {
  chrome.sidePanel.open({ tabId: tab.id });
});

// Handle messages from content script and side panel
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type === "OPEN_SIDEPANEL") {
    chrome.sidePanel.open({ tabId: sender.tab.id });
    // Relay the repo URL to the side panel
    chrome.runtime.sendMessage({
      type: "ANALYZE_REPO",
      repoUrl: message.repoUrl,
    });
    sendResponse({ success: true });
  }

  if (message.type === "FETCH_ANALYSIS") {
    fetchAnalysis(message.repoUrl)
      .then((data) => sendResponse({ success: true, data }))
      .catch((err) => sendResponse({ success: false, error: err.message }));
    return true; // Keep channel open for async response
  }
});

async function fetchAnalysis(repoUrl) {
  // Check extension storage cache first
  const cacheKey = `gitscope:${repoUrl}`;
  const cached = await chrome.storage.local.get(cacheKey);

  if (cached[cacheKey]) {
    const { data, timestamp } = cached[cacheKey];
    // Cache valid for 1 hour
    if (Date.now() - timestamp < 3600000) {
      return { ...data, cached: true };
    }
  }

  const response = await fetch(`${API_BASE}/analyze`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ repo_url: repoUrl }),
  });

  if (!response.ok) {
    const err = await response.json();
    throw new Error(err.detail || "Analysis failed");
  }

  const data = await response.json();

  // Save to extension storage
  await chrome.storage.local.set({
    [cacheKey]: { data, timestamp: Date.now() },
  });

  return data;
}
