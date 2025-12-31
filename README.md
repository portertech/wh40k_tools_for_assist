# WH40k Tools for Assist _(Custom Integration for Home Assistant)_

Bring the grim darkness of the far future to your Home Assistant! This custom integration provides Warhammer 40,000 lore tools for LLM-backed Assist, allowing your AI assistant to answer questions about the Warhammer 40k universe.

## Features

* **🛡️ Warhammer 40k Lexicanum** - Concise, curated lore from the community-maintained wiki
* **📖 Warhammer 40k Fandom Wiki** - Detailed, comprehensive articles from the largest WH40k wiki
* **📜 Wahapedia** - 10th edition game rules, mechanics, stratagems, and faction-specific rules

Each tool is optional and configurable via the integrations UI. No API keys required!

A caching layer reduces latency on repeated requests for the same information within a 2-hour period.

---

## Installation

### Install via HACS (recommended)

Have [HACS](https://hacs.xyz/) installed, this will allow you to update easily.

* Add WH40k Tools for Assist to HACS as a custom repository:
  - In HACS, go to **Integrations**
  - Click the three dots in the top right and select **Custom repositories**
  - Add `https://github.com/portertech/wh40k_tools_for_assist` as a custom repository
  - Category: **Integration**

* Click **Download** on the `WH40k Tools for Assist` integration.
* Restart Home Assistant.

<details><summary>Manual Install</summary>

* Copy the `wh40k_tools_for_assist` folder from [latest release](https://github.com/portertech/wh40k_tools_for_assist/releases/latest) to the [
  `custom_components` folder](https://developers.home-assistant.io/docs/creating_integration_file_structure/#where-home-assistant-looks-for-integrations) in your config directory.
* Restart Home Assistant.

</details>

## Integration Configuration

After installation, configure the integration through Home Assistant's UI:

1. Go to `Settings` → `Devices & Services`.
2. Click `Add Integration`.
3. Search for `WH40k Tools for Assist`.
4. Follow the setup wizard to enable your desired lore sources.

## Conversation Agent Configuration

Once the integration is installed and configured, you will need to enable it within your Conversation Agent entities.

For the Ollama and OpenAI Conversation integrations, this can be found within your Conversation Agent configuration options, beneath
the `Control Home Assistant` heading. Enable the following API:

- **Warhammer 40k Lore**

Now you can ask your assistant questions like:
- "Who is the Emperor of Mankind?"
- "Tell me about the Horus Heresy"
- "What are Space Marines?"
- "Explain the Chaos Gods"
- "What is the Eye of Terror?"
- "How does the shooting phase work?"
- "What stratagems do Space Marines have?"

---

## Tools

### 🛡️ Warhammer 40k Lexicanum

Searches the [Warhammer 40k Lexicanum](https://wh40k.lexicanum.com), a community-maintained wiki focused on providing concise, well-sourced information about the Warhammer 40,000 universe.

#### Requirements

* No API key required
* Uses the public MediaWiki API

#### Configuration Steps

1. Select "Warhammer 40k Lexicanum" during setup
2. Configure the number of results to return (1-20)

#### Options

| Setting             | Required | Default | Description                     |
|---------------------|----------|---------|---------------------------------|
| `Number of Results` | ✅        | `1`     | Number of articles to return    |

---

### 📖 Warhammer 40k Fandom Wiki

Searches the [Warhammer 40k Fandom Wiki](https://warhammer40k.fandom.com), the largest and most comprehensive Warhammer 40,000 wiki with detailed articles covering all aspects of the lore.

#### Requirements

* No API key required
* Uses the public MediaWiki API

#### Configuration Steps

1. Select "Warhammer 40k Fandom" during setup
2. Configure the number of results to return (1-20)

#### Options

| Setting             | Required | Default | Description                     |
|---------------------|----------|---------|---------------------------------|
| `Number of Results` | ✅        | `1`     | Number of articles to return    |

---

### 📜 Wahapedia

Searches [Wahapedia](https://wahapedia.ru/wh40k10ed/) for Warhammer 40k 10th edition game rules. Look up game mechanics, phase rules, stratagems, abilities, detachment rules, and faction-specific rules.

#### Requirements

* No API key required
* Scrapes and caches Wahapedia pages (24-hour cache)

#### Configuration Steps

1. Select "Wahapedia" during setup
2. Configure the number of results to return (1-10)

#### Options

| Setting             | Required | Default | Description                     |
|---------------------|----------|---------|---------------------------------|
| `Number of Results` | ✅        | `3`     | Number of rule sections to return |

#### Supported Factions

The Wahapedia tool supports faction-specific rules for all major factions including:

- Astra Militarum, Adeptus Mechanicus, Adeptus Custodes, Adepta Sororitas
- Space Marines, Blood Angels, Dark Angels, Black Templars, Space Wolves, Deathwatch, Grey Knights
- Imperial Knights, Imperial Agents
- Chaos Space Marines, Death Guard, Thousand Sons, World Eaters, Chaos Daemons, Chaos Knights
- Aeldari, Drukhari, Harlequins
- Tyranids, Genestealer Cults
- Orks, Necrons, T'au Empire, Leagues of Votann

---

## Usage Examples

Ask your Home Assistant about:

### Lore (Lexicanum & Fandom)
- **Factions**: "What are the Adeptus Mechanicus?", "Tell me about Orks"
- **Characters**: "Who is Roboute Guilliman?", "Explain Abaddon the Despoiler"
- **Events**: "What was the Horus Heresy?", "Describe the Fall of Cadia"
- **Locations**: "Where is Terra?", "What is Commorragh?"
- **Technology**: "What is a Bolter?", "Explain Warp travel"
- **Concepts**: "What is the Warp?", "Describe the Astronomican"

### Game Rules (Wahapedia)
- **Core Rules**: "How does the shooting phase work?", "Explain mortal wounds"
- **Stratagems**: "What stratagems can Space Marines use?"
- **Faction Rules**: "What are the Astra Militarum army rules?"
- **Detachments**: "Tell me about the Gladius Task Force detachment"
- **Abilities**: "What is the Feel No Pain ability?"

The integration will search enabled sources based on the query, giving your assistant access to both comprehensive lore and game rules.

---

## Acknowledgements

This integration is a fork of [Tools for Assist](https://github.com/skye-harris/llm_intents) by [@skye-harris](https://github.com/skye-harris), refactored to focus specifically on Warhammer 40k lore tools.

[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

---

For the Emperor! 🛡️
