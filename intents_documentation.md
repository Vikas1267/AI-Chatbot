# 📚 ARIA — Intents Documentation

> Complete reference for all 20 intent categories supported by the ARIA chatbot engine.
> Each entry shows the intent tag, 3 example trigger phrases, a sample bot response, and the matching strategy notes.

---

## Intent Index

| # | Tag | Description |
|---|-----|-------------|
| 1 | [greeting](#1-greeting) | Welcome messages |
| 2 | [goodbye](#2-goodbye) | Farewell messages |
| 3 | [thanks](#3-thanks) | Gratitude expressions |
| 4 | [name](#4-name) | Chatbot identity queries |
| 5 | [hours](#5-hours) | Availability/business hours |
| 6 | [products](#6-products) | Product/service catalog |
| 7 | [pricing](#7-pricing) | Cost and rate information |
| 8 | [complaint](#8-complaint) | Dissatisfaction handling |
| 9 | [help](#9-help) | Capability overview |
| 10 | [weather](#10-weather) | Weather information |
| 11 | [joke](#11-joke) | Humor and entertainment |
| 12 | [news](#12-news) | Current events |
| 13 | [reminder](#13-reminder) | Reminder requests |
| 14 | [order_status](#14-order_status) | Order tracking |
| 15 | [return_policy](#15-return_policy) | Returns and refunds |
| 16 | [shipping](#16-shipping) | Delivery information |
| 17 | [contact](#17-contact) | Support contact details |
| 18 | [about_us](#18-about_us) | Company background |
| 19 | [capabilities](#19-capabilities) | ARIA's feature set |
| 20 | [fallback](#20-fallback) | Unrecognized inputs |

---

## 1. `greeting`

**Description:** Triggered when a user opens or initiates a conversation with a friendly hello.

**Pattern count:** 10 patterns | **Response count:** 4

### Example Triggers
| # | Trigger Phrase |
|---|---------------|
| 1 | "Hello" |
| 2 | "Hey there" |
| 3 | "Good morning" |

### Sample Response
> *"Hello! Welcome! How can I assist you today? 😊"*

**NLP Notes:** Commonly stems to "hello", "hi", "good" — high-frequency short tokens. Confidence typically moderate (~0.24) due to short patterns.

---

## 2. `goodbye`

**Description:** Triggered when the user signals the end of the conversation.

**Pattern count:** 10 patterns | **Response count:** 4

### Example Triggers
| # | Trigger Phrase |
|---|---------------|
| 1 | "Bye" |
| 2 | "See you later" |
| 3 | "Take care" |

### Sample Response
> *"Goodbye! Have a wonderful day! 👋"*

**NLP Notes:** Farewell tokens ("bye", "farewell", "later") are distinctive — typically recognized cleanly even at short lengths.

---

## 3. `thanks`

**Description:** Triggered when a user expresses gratitude or appreciation.

**Pattern count:** 10 patterns | **Response count:** 4

### Example Triggers
| # | Trigger Phrase |
|---|---------------|
| 1 | "Thank you" |
| 2 | "Appreciate it" |
| 3 | "Much appreciated" |

### Sample Response
> *"You're welcome! Happy to help anytime. 😊"*

**NLP Notes:** Strong stem overlap on "thank", "appreci" — usually recognized with high confidence.

---

## 4. `name`

**Description:** Triggered when the user asks who they're talking to or wants the chatbot to introduce itself.

**Pattern count:** 8 patterns | **Response count:** 4

### Example Triggers
| # | Trigger Phrase |
|---|---------------|
| 1 | "What is your name?" |
| 2 | "Who are you?" |
| 3 | "Introduce yourself" |

### Sample Response
> *"I'm ARIA — Adaptive Responsive Intelligent Assistant! Nice to meet you! 🤖"*

**NLP Notes:** Key stems: "name", "call", "who", "introduc". Ambiguity possible with `about_us` ("who are you" vs "tell me about your company") — resolved by cosine similarity.

---

## 5. `hours`

**Description:** Triggered when users ask about operating hours, availability, or when they can chat with ARIA.

**Pattern count:** 8 patterns | **Response count:** 4

### Example Triggers
| # | Trigger Phrase |
|---|---------------|
| 1 | "What are your hours?" |
| 2 | "Are you available 24/7?" |
| 3 | "When can I talk to you?" |

### Sample Response
> *"I'm always here for you, 24 hours a day, 7 days a week. No holidays!"*

**NLP Notes:** Key stems: "hour", "open", "time", "avail". Verified confidence ~0.49 on "what are your hours" in testing.

---

## 6. `products`

**Description:** Triggered when a user inquires about what products or services are available.

**Pattern count:** 9 patterns | **Response count:** 4

### Example Triggers
| # | Trigger Phrase |
|---|---------------|
| 1 | "What products do you offer?" |
| 2 | "What do you sell?" |
| 3 | "List your products" |

### Sample Response
> *"We offer a wide range of products including electronics, clothing, home goods, and more! Ask me about a specific category for details."*

**NLP Notes:** Key stems: "product", "sell", "offer", "catalog", "item". Strong overlap with `pricing` mitigated by distinct product-specific vocab.

---

## 7. `pricing`

**Description:** Triggered when a user asks about costs, prices, or rates.

**Pattern count:** 9 patterns | **Response count:** 4

### Example Triggers
| # | Trigger Phrase |
|---|---------------|
| 1 | "How much does it cost?" |
| 2 | "What are your rates?" |
| 3 | "Pricing information" |

### Sample Response
> *"Our pricing varies by product and service. Generally, we offer competitive rates starting from $9.99. Would you like specifics?"*

**NLP Notes:** Key stems: "cost", "price", "rate", "charg", "expens". Distinguished from `products` by financial/monetary terms.

---

## 8. `complaint`

**Description:** Triggered when a user expresses dissatisfaction, frustration, or wants to report a problem.

**Pattern count:** 10 patterns | **Response count:** 4

### Example Triggers
| # | Trigger Phrase |
|---|---------------|
| 1 | "I have a complaint" |
| 2 | "I'm very disappointed" |
| 3 | "Bad experience" |

### Sample Response
> *"I'm truly sorry to hear that! Your feedback is important to us. Could you tell me more about what went wrong so I can help resolve it?"*

**NLP Notes:** Key stems: "complaint", "disappoint", "frustrat", "bad", "terribl". Negative sentiment patterns are well-distinguished from other intents.

---

## 9. `help`

**Description:** Triggered when users ask for guidance, assistance, or want to know what ARIA can do.

**Pattern count:** 10 patterns | **Response count:** 4

### Example Triggers
| # | Trigger Phrase |
|---|---------------|
| 1 | "Help" |
| 2 | "I need assistance" |
| 3 | "How do I use this?" |

### Sample Response
> *"Of course! I'm here to help. You can ask me about products, pricing, orders, weather, jokes, news, and much more. What do you need?"*

**NLP Notes:** Key stems: "help", "assist", "stuck", "guid". Overlaps with `capabilities` on "what can you do" — both are listed patterns, cosine similarity differentiates.

---

## 10. `weather`

**Description:** Triggered when users ask about weather conditions or forecasts.

**Pattern count:** 9 patterns | **Response count:** 4

### Example Triggers
| # | Trigger Phrase |
|---|---------------|
| 1 | "What's the weather like?" |
| 2 | "Is it going to rain?" |
| 3 | "Weather forecast" |

### Sample Response
> *"I don't have real-time weather data, but I'd recommend checking weather.com or your local weather app for the latest forecast! 🌤️"*

**NLP Notes:** Key stems: "weather", "rain", "temperatur", "forecastsunni". Highly distinctive domain vocabulary — typically high confidence.

---

## 11. `joke`

**Description:** Triggered when a user requests humor, jokes, or wants to be entertained.

**Pattern count:** 9 patterns | **Response count:** 4

### Example Triggers
| # | Trigger Phrase |
|---|---------------|
| 1 | "Tell me a joke" |
| 2 | "Make me laugh" |
| 3 | "Cheer me up" |

### Sample Response
> *"Why can't you give Elsa a balloon? Because she'll let it go! ❄️ Hope that brightened your day!"*

**NLP Notes:** Key stems: "joke", "laugh", "funni", "cheer". Very distinctive vocabulary — high confidence (~0.68) confirmed in verification testing.

---

## 12. `news`

**Description:** Triggered when a user asks about current events, headlines, or what's happening in the world.

**Pattern count:** 9 patterns | **Response count:** 4

### Example Triggers
| # | Trigger Phrase |
|---|---------------|
| 1 | "What's in the news?" |
| 2 | "Latest updates" |
| 3 | "News headlines" |

### Sample Response
> *"I don't have access to live news feeds, but I'd recommend BBC News, CNN, or Google News for the latest headlines! 📰"*

**NLP Notes:** Key stems: "news", "head", "latest", "current". Domain-specific vocab leads to reliable recognition.

---

## 13. `reminder`

**Description:** Triggered when a user wants ARIA to remember something or set a reminder.

**Pattern count:** 9 patterns | **Response count:** 4

### Example Triggers
| # | Trigger Phrase |
|---|---------------|
| 1 | "Set a reminder" |
| 2 | "Remind me to call back at 3pm" |
| 3 | "Don't let me forget" |

### Sample Response
> *"I'd love to help with reminders! For now, I'd suggest using your phone's built-in reminder app or Google Calendar for reliable alerts. 📅"*

**NLP Notes:** Key stems: "remind", "schedul", "alert", "forget". Unique action-oriented vocabulary.

---

## 14. `order_status`

**Description:** Triggered when a user wants to track, check, or update the status of an order.

**Pattern count:** 9 patterns | **Response count:** 4

### Example Triggers
| # | Trigger Phrase |
|---|---------------|
| 1 | "Where is my order?" |
| 2 | "Track my order" |
| 3 | "My order hasn't arrived" |

### Sample Response
> *"Order tracking is easy! Share your order number here, or visit our website's 'My Orders' section to get real-time updates. 🚚"*

**NLP Notes:** Key stems: "order", "track", "arriv", "status". Confidence ~0.93 on "my order is late" — highest in verification suite. Distinct from `shipping` by focus on specific order status vs. general shipping policies.

---

## 15. `return_policy`

**Description:** Triggered when users ask about returning items, refunds, or exchange policies.

**Pattern count:** 9 patterns | **Response count:** 4

### Example Triggers
| # | Trigger Phrase |
|---|---------------|
| 1 | "What is your return policy?" |
| 2 | "Can I get a refund?" |
| 3 | "How long do I have to return?" |

### Sample Response
> *"We offer a hassle-free 30-day return policy! Items must be in original condition. Visit our Returns Center to initiate a return. 🔄"*

**NLP Notes:** Key stems: "return", "refund", "exchang", "policy". Distinct from `order_status` by policy/process focus rather than tracking.

---

## 16. `shipping`

**Description:** Triggered when users ask about delivery timelines, shipping costs, or delivery options.

**Pattern count:** 9 patterns | **Response count:** 4

### Example Triggers
| # | Trigger Phrase |
|---|---------------|
| 1 | "How long does shipping take?" |
| 2 | "Do you offer free shipping?" |
| 3 | "Express shipping available?" |

### Sample Response
> *"We offer standard (5-7 days), express (2-3 days), and overnight shipping! Free shipping on orders over $50. 🚚"*

**NLP Notes:** Key stems: "ship", "deliver", "express", "standard". Overlaps slightly with `order_status` but shipping focuses on policies/options, not individual order tracking.

---

## 17. `contact`

**Description:** Triggered when a user wants to reach a human agent or find support contact details.

**Pattern count:** 9 patterns | **Response count:** 4

### Example Triggers
| # | Trigger Phrase |
|---|---------------|
| 1 | "How can I contact you?" |
| 2 | "What is your phone number?" |
| 3 | "Talk to a human" |

### Sample Response
> *"You can reach us via email at support@example.com, by phone at 1-800-EXAMPLE, or through our live chat. We're here Mon-Fri 9AM-6PM EST! 📞"*

**NLP Notes:** Key stems: "contact", "phone", "email", "reach", "human". Unique combination of contact-channel vocabulary.

---

## 18. `about_us`

**Description:** Triggered when users want to know more about the company or ARIA's background.

**Pattern count:** 9 patterns | **Response count:** 4

### Example Triggers
| # | Trigger Phrase |
|---|---------------|
| 1 | "Tell me about your company" |
| 2 | "What does your company do?" |
| 3 | "Tell me more about ARIA" |

### Sample Response
> *"We're a technology company dedicated to making AI assistance accessible to everyone! ARIA is our flagship intelligent assistant. 🌟"*

**NLP Notes:** Key stems: "compani", "about", "busi", "background". Distinguished from `name` intent by company/business context tokens.

---

## 19. `capabilities`

**Description:** Triggered when users ask what ARIA can do, its features, or its knowledge scope.

**Pattern count:** 9 patterns | **Response count:** 4

### Example Triggers
| # | Trigger Phrase |
|---|---------------|
| 1 | "What can you do?" |
| 2 | "What are your capabilities?" |
| 3 | "Show me what you can do" |

### Sample Response
> *"I can help with: answering questions, product info, order tracking, return policies, shipping info, telling jokes, weather tips, news sources, setting reminders, and general conversation! 🤖"*

**NLP Notes:** Key stems: "capabilit", "can", "featur", "skill". Overlaps with `help` ("what can you do" is shared pattern). Cosine similarity and pattern weighting resolve ambiguity.

---

## 20. `fallback`

**Description:** Activated when no intent matches with sufficient confidence (threshold < 0.15), or for intentionally unrecognizable input patterns.

**Pattern count:** 4 patterns (intentionally low) | **Response count:** 4

### Example Triggers
| # | Trigger Phrase |
|---|---------------|
| 1 | "asdfgh" (gibberish) |
| 2 | Completely off-topic input |
| 3 | Heavily misspelled/unrelated text |

### Sample Response
> *"I'm not quite sure I understood that. Could you rephrase or ask something else? I'm here to help! 🤔"*

**NLP Notes:** This intent is a safety net. The 4 intentionally nonsense patterns ensure this intent scores very low in cosine similarity against normal inputs, so it only triggers via the confidence threshold, not direct pattern matching.

---

## NLP Pipeline Summary

```
User Input
    │
    ▼
word_tokenize (NLTK punkt)
    │
    ▼
Lowercase + PorterStemmer + remove stopwords
    │
    ▼
Bag-of-Words vector (vocabulary from all intent patterns)
    │
    ▼
Cosine Similarity vs. each intent's pattern vector
    │
    ├── max_similarity >= 0.15 → matched intent → random response
    └── max_similarity < 0.15  → fallback intent → fallback response
```

---

*ARIA Intents Documentation v1.0 · WeIntern Week 2 · 2026*
