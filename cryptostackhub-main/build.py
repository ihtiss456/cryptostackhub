#!/usr/bin/env python3
"""CRYPTOSTACKHUB static site generator — builds the full premium blog site."""
import json, os, shutil, re

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = ROOT  # build in place

CATS = {
    "defi":    dict(slug="defi",            label="DeFi & Crypto Education", short="DeFi",
                    cls="cat-defi", tone="var(--defi)",
                    tint2="rgba(45,212,191,.38)", tint3="rgba(96,165,250,.28)",
                    tagline="Decentralized finance, explained from first principles",
                    desc="Clear, honest guides to DeFi — wallets, staking, liquidity, stablecoins and staying safe on-chain."),
    "dev":     dict(slug="developers",      label="Blockchain Development", short="Developers",
                    cls="cat-dev", tone="var(--dev)",
                    tint2="rgba(167,139,250,.38)", tint3="rgba(94,234,212,.26)",
                    tagline="Ship secure smart contracts and dApps",
                    desc="Engineering deep-dives for builders: Solidity, EVM internals, testing, security and scaling."),
    "tax":     dict(slug="tax-compliance",  label="Crypto Tax & Compliance", short="Tax",
                    cls="cat-tax", tone="var(--tax)",
                    tint2="rgba(245,185,66,.38)", tint3="rgba(244,114,182,.22)",
                    tagline="Stay compliant without the headache",
                    desc="Practical tax and compliance guidance for crypto users and startups, in plain language."),
    "gaming":  dict(slug="gaming-nfts",     label="Web3 Gaming & NFTs", short="Gaming & NFTs",
                    cls="cat-gaming", tone="var(--gaming)",
                    tint2="rgba(244,114,182,.38)", tint3="rgba(167,139,250,.26)",
                    tagline="Where games meet ownership",
                    desc="Web3 gaming, NFT utility, player-owned economies and how to spot the rug before it pulls."),
}
AUTHORS = {
    "research": {"slug":"cryptostackhub-research","name":"CryptoStackHub Research Desk","role":"DeFi & Crypto Education Editors","bio":"The CryptoStackHub Research Desk produces first-principles explainers on DeFi, wallets, staking, liquidity and on-chain security, with a focus on clear mechanisms and practical risk."},
    "engineering": {"slug":"cryptostackhub-engineering","name":"CryptoStackHub Engineering Desk","role":"Blockchain Development Editors","bio":"The CryptoStackHub Engineering Desk covers Solidity, EVM internals, testing, smart-contract security and scaling for builders who want practical, implementation-focused guidance."},
    "compliance": {"slug":"cryptostackhub-compliance","name":"CryptoStackHub Compliance Desk","role":"Crypto Tax & Compliance Editors","bio":"The CryptoStackHub Compliance Desk explains crypto tax, recordkeeping and regulatory topics in plain language, emphasizing jurisdictional differences, documentation and responsible research."},
    "gaming": {"slug":"cryptostackhub-gaming","name":"CryptoStackHub Gaming Desk","role":"Web3 Gaming & NFT Editors","bio":"The CryptoStackHub Gaming Desk analyzes player-owned assets, NFT utility, game economies and Web3 gaming risks without confusing marketing promises with durable utility."},
}
AUTHOR_BY_CAT = {"defi":"research","dev":"engineering","tax":"compliance","gaming":"gaming"}

ICONS = {
    "defi":   '<svg viewBox="0 0 24 24" fill="none" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2 3 7v10l9 5 9-5V7l-9-5z"/><path d="M12 22V12"/><path d="m3 7 9 5 9-5"/></svg>',
    "dev":    '<svg viewBox="0 0 24 24" fill="none" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="m8 6-6 6 6 6"/><path d="m16 6 6 6-6 6"/><path d="m13 4-2 16"/></svg>',
    "tax":    '<svg viewBox="0 0 24 24" fill="none" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="2" width="16" height="20" rx="2"/><path d="M8 6h8M8 10h8M8 14h4"/><path d="M15 14l4 4m0-4-4 4"/></svg>',
    "gaming": '<svg viewBox="0 0 24 24" fill="none" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="6" width="20" height="12" rx="6"/><path d="M7 10v4M5 12h4"/><circle cx="16" cy="10.5" r="1"/><circle cx="18.5" cy="13.5" r="1"/></svg>',
}
LOGO_SVG = '<img src="/assets/images/cryptostackhub-logo.png" alt="CryptoStackHub logo">'

CODE_SNIPPET = '''<pre><code>// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

contract Vault {
    mapping(address => uint256) public balances;

    function deposit() external payable {
        balances[msg.sender] += msg.value;
    }

    function withdraw(uint256 amount) external {
        require(balances[msg.sender] >= amount, "insufficient");
        balances[msg.sender] -= amount;   // effects before interaction
        (bool ok, ) = msg.sender.call{value: amount}("");
        require(ok, "transfer failed");
    }
}</code></pre>'''

# ---------------------------------------------------------------- articles
def A(slug, title, cat, desc, read, kw, sections, takeaways):
    return dict(slug=slug, title=title, cat=cat, desc=desc, read=read,
                keywords=kw, sections=sections, takeaways=takeaways,
                author_key=AUTHOR_BY_CAT[cat])

def S(title, *blocks): return dict(title=title, blocks=list(blocks))

ARTICLES = [
# ---------------- DeFi ----------------
A("what-is-defi","What Is DeFi?","defi",
  "Decentralized finance rebuilds lending, trading and savings on open blockchains. Here is how it works, why it matters, and where the real risks live.",
  "9 min","defi introduction decentralized finance basics",
  [S("A financial system without the middlemen",
     "Decentralized finance — DeFi — is a set of financial applications built on public blockchains, most famously Ethereum. Instead of a bank holding your deposits and deciding who gets a loan, smart contracts (self-executing code) hold the funds and enforce the rules. Anyone with a wallet and an internet connection can lend, borrow, trade or earn yield, 24/7, without filling in a single form.",
     "The stack typically has three layers: the settlement layer (the blockchain itself), the protocol layer (smart contracts that define products like exchanges or money markets), and the application layer (the websites and wallets you actually click on)."),
   S("The core building blocks",
     "Almost everything in DeFi is composed from a handful of primitives:",
     "list:Decentralized exchanges (DEXs) — swap tokens directly from your wallet via liquidity pools|Lending protocols — supply assets to earn interest, or borrow against collateral|Stablecoins — tokens pegged to fiat currencies that make DeFi usable day to day|Staking & restaking — locking tokens to secure networks and earn rewards|Derivatives & structured products — on-chain options, perps and yield strategies"),
   S("Why people actually use it",
     "DeFi offers genuine advantages: global access without permission, transparent rules anyone can audit, near-instant settlement, and yields generated by real protocol activity rather than opaque bank balance sheets. For users in countries with unstable currencies or limited banking, stablecoins and DeFi savings can be life-changing.",
     "It is also composable: protocols snap together like Lego bricks, so a single transaction can swap an asset, lend it out, and stake the receipt token in one go."),
   S("The risks nobody should skip",
     "DeFi is not a free lunch. Smart contract bugs and exploits have drained billions. Oracle manipulation, governance attacks, impermanent loss and plain old scams are all part of the landscape. Prices are volatile, and there is usually no customer support line and no deposit insurance.",
     "list:Only use audited, battle-tested protocols with meaningful TVL|Never invest more than you can afford to lose entirely|Verify contract addresses from official sources, never from DMs|Start small and treat early experiments as tuition"),
  ],
  ["DeFi replaces financial intermediaries with open smart contracts","Lending, DEXs, stablecoins and staking are the core primitives","Accessibility and transparency are real — so are the risks","Security habits matter more than chasing the highest APY"]),

A("how-staking-works","How Staking Works","defi",
  "Staking secures proof-of-stake networks and pays you for it. Learn how validators, delegators, lockups and slashing actually work before you commit funds.",
  "8 min","staking proof of stake validators rewards",
  [S("From miners to validators",
     "Proof-of-stake replaces energy-hungry mining with economic security. Validators lock up (stake) the network's native token as collateral, then propose and attest to new blocks. Honest behavior earns rewards; dishonest behavior gets part of the stake destroyed — a penalty called slashing.",
     "Ethereum, Solana, Cosmos and most modern chains use some variant of this design. The token you stake is simultaneously an investment, a security deposit, and a vote in the network's consensus."),
   S("The three ways to stake",
     "list:Solo validating — run your own node (32 ETH on Ethereum); maximum control and rewards, maximum responsibility|Staking-as-a-service — a provider runs the node, you keep the keys to your funds; small fee, moderate trust|Pooled / liquid staking — deposit any amount into a pool and receive a liquid staking token (like stETH) you can still use in DeFi"),
   S("Where the yield comes from",
     "Staking rewards come from two real sources: new token issuance (protocol inflation directed to stakers) and transaction fees (including MEV tips) paid by users of the network. This is why staking is often called 'real yield' — it is revenue from network activity, not printed ponzi points."),
   S("Risks to understand before staking",
     "list:Slashing — rare but real; validator downtime or double-signing burns stake|Lockups — some networks require unbonding periods of days or weeks|Price risk — a 5% APY does not help if the token falls 50%|Smart contract risk — liquid staking protocols add a layer of code risk|Centralization — choosing dominant providers can weaken the network itself")],
  ["Staking pays for securing proof-of-stake networks with economic collateral","Solo, delegated and liquid staking trade control against convenience","Yield comes from issuance plus transaction fees — real network revenue","Slashing, lockups and price risk are the trade-offs to weigh"]),

A("yield-farming-vs-staking","Yield Farming vs. Staking","defi",
  "Both promise passive income on your crypto, but they work completely differently. A clear breakdown of mechanics, risk profiles and when each makes sense.",
  "7 min","yield farming staking comparison passive income",
  [S("Two different jobs, two different paychecks",
     "Staking pays you for securing a blockchain. Yield farming pays you for providing liquidity or capital to a DeFi protocol. The distinction matters because the risks are entirely different: stakers worry about slashing and lockups; farmers worry about impermanent loss, exploit risk and unsustainable reward emissions."),
   S("How yield farming actually works",
     "You deposit assets — often a pair of tokens — into a liquidity pool or lending market. In return you earn a share of trading fees or interest, plus (frequently) incentive tokens the protocol prints to attract liquidity. The advertised APY is usually a blend of both, and the incentive portion can collapse the moment emissions slow or the reward token dumps."),
   S("Comparing the risk profiles",
     "list:Staking: protocol-level risk, slashing, lockup periods, price volatility of the staked asset|Farming: smart contract risk, impermanent loss, reward-token inflation, rug pulls on newer pools|Both: market risk — yield denominated in a falling asset is still a loss in fiat terms"),
   S("Which one is right for you?",
     "As a rough heuristic: staking suits long-term holders of a network's token who want low-maintenance, relatively conservative yield. Farming suits active users who understand pool mechanics, monitor positions, and size into risk appropriately. If an APY looks too good to be true — triple digits on a new pool — it almost always is.")],
  ["Staking = securing a network; farming = supplying liquidity to a protocol","Farming yields are often inflated by unsustainable token emissions","Impermanent loss and exploit risk are unique to farming","Match the strategy to your time horizon and risk tolerance"]),

A("impermanent-loss-explained","Impermanent Loss Explained","defi",
  "The most misunderstood risk in DeFi. With clear math and real examples, learn when providing liquidity beats holding — and when it quietly bleeds you.",
  "10 min","impermanent loss liquidity pool amm math",
  [S("The problem in one sentence",
     "When you deposit two tokens into an automated market maker (AMM) pool, the pool constantly rebalances you into whichever token is underperforming — so if prices move apart, you end up worse off than simply holding. That difference is impermanent loss."),
   S("A concrete example",
     "You deposit $1,000 of ETH and $1,000 of USDC into a 50/50 pool. ETH doubles. Arbitrage traders buy your cheaper ETH from the pool until prices match the market — leaving you with less ETH and more USDC. Your position is now worth roughly $2,414, while simply holding would be worth $3,000. The ~$586 gap is impermanent loss.",
     "The loss is called 'impermanent' because if prices return to the entry ratio, it disappears. Realize it by withdrawing at the wrong time and it becomes very permanent."),
   S("When fees and rewards beat the loss",
     "Impermanent loss is not automatically bad. Pools that generate strong fee revenue — high volume relative to TVL — can out-earn the loss, especially on correlated pairs (like two stablecoins, where IL is near zero). The question is always: do fees plus incentives exceed IL plus risk?",
     "list:Correlated pairs (stables, LST/ETH): minimal IL, modest fees|Volatile blue-chip pairs (ETH/wBTC): meaningful IL, strong volume|Exotic pairs: extreme IL risk, often subsidized by inflationary rewards"),
   S("How LPs manage it",
     "list:Prefer correlated or pegged pairs for stability|Use concentrated-liquidity ranges thoughtfully — tighter ranges amplify both fees and IL|Track your position's hold-vs-LP performance, not just the APY banner|Size positions so a worst-case divergence is survivable")],
  ["IL happens because AMMs rebalance you into the underperforming asset","It grows with price divergence — a 2x move costs ~5.7% vs holding","Correlated pairs and fee income are the main defenses","Always compare LP returns against a simple buy-and-hold baseline"]),

A("best-defi-wallets-compared","Best DeFi Wallets Compared","defi",
  "Hot wallets, hardware wallets, smart-contract wallets — a practical comparison of the leading options for DeFi users, and how to choose your setup.",
  "11 min","defi wallets comparison metamask ledger hardware wallet",
  [S("What a DeFi wallet actually needs to do",
     "A DeFi wallet is more than a place to store tokens. It is your identity layer: it signs transactions, connects to dApps, manages approvals, and — ideally — protects you from your own mistakes. The right choice depends on how much you hold and how actively you use protocols."),
   S("The three categories",
     "list:Browser hot wallets (e.g. MetaMask, Rabby, Phantom) — fastest UX, best dApp compatibility, but your keys live on an internet-connected device|Hardware wallets (e.g. Ledger, Trezor) — keys stay offline; pair one with a hot wallet interface for a strong security baseline|Smart-contract wallets (e.g. Safe) — multi-signature, spending limits, social recovery; the gold standard for treasuries and serious holdings"),
   S("Features that separate the best from the rest",
     "list:Transaction simulation — preview what a transaction does before signing|Approval management — see and revoke token allowances easily|Multi-chain support with clear network warnings|Open-source code and a strong audit history|Hardware and multi-sig compatibility"),
   S("A sensible setup for most people",
     "Use a hardware wallet as your vault for long-term holdings. Connect it to a reputable browser wallet for occasional DeFi use. Keep a small separate hot wallet for experiments with new protocols. And whatever you do: never type your seed phrase into a website, ever.")],
  ["Match the wallet type to your activity: vault, daily driver, or experimental","Hardware + hot wallet pairing is the best security/convenience balance","Transaction simulation and approval management are must-have features","Your seed phrase is the keys to everything — protect it accordingly"]),

A("how-to-read-defi-audit","How to Read a DeFi Protocol's Smart Contract Audit","defi",
  "An audit badge means nothing if you can't read the report. Learn what auditors actually check, what severity ratings mean, and the red flags to look for.",
  "9 min","smart contract audit security due diligence",
  [S("Why 'audited' doesn't mean 'safe'",
     "An audit is a point-in-time review of specific code, not a guarantee. Protocols have been exploited days after audits, usually through code changed post-audit, economic attacks outside the audit scope, or issues the auditors simply missed. Reading the actual report tells you what was — and was not — covered."),
   S("The five things to check first",
     "list:Who audited it — reputable firms publish track records and methodology|When — anything over ~12 months old, or before major upgrades, is stale|Scope — which contracts and commit hashes were actually reviewed|Findings — how many critical/high issues, and were they fixed or just 'acknowledged'?|Residual risks — good reports list what they could NOT verify"),
   S("Reading severity ratings",
     "Critical and high-severity findings (reentrancy, oracle manipulation, access control flaws) must be marked 'resolved' or 'fixed' with a verified commit. 'Acknowledged' means the team chose to accept the risk — read their reasoning carefully. Medium and low findings matter less individually but reveal code quality culture."),
   S("Red flags that should stop you",
     "list:No audit at all for a protocol holding meaningful TVL|Audits of a different codebase than what's deployed|Admin keys that can drain funds with no timelock or multi-sig|An anonymous team with upgradeable proxies and no governance delay|Fixes claimed but not verifiable on-chain or in the repo")],
  ["Audits are point-in-time and scoped — read the coverage, not the badge","Critical findings must be resolved, not merely acknowledged","Check that audited code matches deployed contracts","Admin key structure matters as much as code quality"]),

A("cex-vs-dex-comparison","Centralized vs. Decentralized Exchanges","defi",
  "Binance or Uniswap? Custody, fees, liquidity, privacy and risk — an honest head-to-head comparison to help you choose where to trade.",
  "8 min","cex dex exchange comparison uniswap binance custody",
  [S("The fundamental difference: custody",
     "A centralized exchange (CEX) holds your crypto for you — you have an IOU, not the assets. A decentralized exchange (DEX) settles trades on-chain directly from your wallet: you keep custody at all times. Every other difference flows from this single design choice."),
   S("Where CEXs win",
     "list:Deep liquidity and tight spreads, especially on large orders|Fiat on/off ramps — bank transfers, cards, local currencies|Familiar UX, customer support, and account recovery|Advanced order types (limit, stop, OCO) at low cost"),
   S("Where DEXs win",
     "list:Self-custody — no exchange can freeze or lose your funds|Permissionless access — no KYC, no geographic blocks|Long-tail assets — any token can be listed and traded|Transparency — reserves and mechanics are auditable on-chain"),
   S("The honest trade-offs",
     "CEXs concentrate counterparty risk: hacks, insolvency and frozen withdrawals have burned users repeatedly. DEXs shift risk to you: smart contract exploits, MEV, slippage on thin pools, and no recourse if you send funds to the wrong place. Many experienced users do both — fiat ramps and large trades on reputable CEXs, then withdraw to self-custody for on-chain activity.")],
  ["CEX = they hold your keys; DEX = you always hold your keys","CEXs offer liquidity, fiat ramps and UX; DEXs offer custody and access","Neither is risk-free — the risks are just different species","Withdraw to self-custody for anything you plan to hold long-term"]),

A("common-defi-scams","Common DeFi Scams (and How to Avoid Them)","defi",
  "Rug pulls, honeypots, phishing, approval exploits — a field guide to the scams that drain wallets, with the exact red flags to watch for.",
  "10 min","defi scams rug pull phishing honeypot security",
  [S("The anatomy of a rug pull",
     "In a classic rug pull, developers launch a token or farm, attract liquidity with huge APYs and influencer hype, then drain the pool or mint themselves a mountain of tokens and dump. Variants include 'soft rugs' — insiders quietly selling into retail buying — which are harder to prove but just as costly."),
   S("The scam playbook",
     "list:Phishing sites — pixel-perfect clones of real dApps, promoted through ads and fake airdrop announcements|Approval exploits — tricking you into signing unlimited token approvals to a malicious contract|Honeypots — tokens you can buy but the contract blocks you from selling|Fake support — 'admins' in DMs asking for your seed phrase to 'fix' an issue|Address poisoning — dust transactions from lookalike addresses hoping you'll copy the wrong one"),
   S("Your defense checklist",
     "list:Bookmark official sites; never click sponsored search ads for dApps|Verify contracts on a block explorer against the official docs|Review every signature request — understand what you're approving|Use a burner wallet for new, unaudited protocols|Revoke stale approvals regularly with an allowance checker|If anyone asks for your seed phrase, it is a scam. Full stop."),
   S("The mindset that saves you",
     "Scams exploit urgency and greed. Any offer that requires you to act now, promises guaranteed returns, or arrives via unsolicited DM should be treated as hostile until proven otherwise. Legitimate protocols never DM you first.")],
  ["Rug pulls, phishing and malicious approvals cause most losses","Never sign what you don't understand; never share your seed phrase","Use burner wallets and revoke approvals as routine hygiene","Urgency + guaranteed returns + unsolicited contact = scam"]),

A("liquidity-pools-first-principles","Liquidity Pools: First Principles","defi",
  "How can you trade without an order book? The math of constant-product AMMs, liquidity providers and price discovery — built up from zero.",
  "12 min","liquidity pools amm constant product uniswap how it works",
  [S("Trading without a counterparty",
     "Traditional exchanges match buyers and sellers via an order book. A liquidity pool replaces the counterparty with a smart contract holding reserves of two tokens. You trade against the pool itself, and a formula — not a market maker — sets the price."),
   S("The constant product formula",
     "The classic AMM keeps the product of its two reserves constant: x × y = k. Buy some of token X and the pool's X reserve shrinks while Y grows, so the next unit of X costs more. Price is simply the ratio of the reserves; every trade moves it. This is why large trades in small pools suffer brutal slippage."),
   S("Who provides the liquidity — and why",
     "Liquidity providers (LPs) deposit both tokens in equal value and receive LP tokens representing their share. Traders pay a fee (commonly 0.05–1%) on every swap, distributed pro-rata to LPs. The incentive is fee income; the risk is impermanent loss when prices diverge."),
   S("Evolutions worth knowing",
     "list:Concentrated liquidity (Uniswap v3) — LPs choose price ranges, multiplying capital efficiency|Stableswap curves — flatter pricing for pegged assets like stablecoins|Weighted pools (Balancer) — ratios beyond 50/50, e.g. 80/20 to reduce IL|Just-in-time liquidity & MEV — the dark forest every LP should understand")],
  ["AMMs replace order books with pooled reserves and a pricing formula","x × y = k means every trade moves the price — depth equals low slippage","LPs earn trading fees but bear impermanent loss","Concentrated liquidity improved efficiency at the cost of active management"]),

A("stablecoins-explained","Stablecoins Explained","defi",
  "Fiat-backed, crypto-backed, algorithmic — the three designs for price-stable crypto, how each can fail, and how to evaluate which to trust.",
  "9 min","stablecoins usdc usdt dai algorithmic fiat backed",
  [S("Why stability is the killer app",
     "Crypto's volatility makes it terrible money for everyday use. Stablecoins solve this by pegging to an external reference — usually the US dollar — combining blockchain settlement (fast, global, 24/7) with fiat-like price stability. They are, by transaction volume, crypto's most-used product."),
   S("The three designs",
     "list:Fiat-backed (USDC, USDT) — each token claims backing by cash and T-bills in a bank; simple and stable, but requires trusting the issuer and its attestations|Crypto-backed (DAI, LUSD) — overcollateralized by on-chain assets like ETH; transparent and censorship-resistant, but capital-inefficient and exposed to collateral crashes|Algorithmic — maintain the peg through code and incentives alone; elegant in theory, and the category that produced Terra/UST's $40B collapse"),
   S("How to evaluate a stablecoin",
     "list:What exactly backs it, and can you verify it? (attestations, on-chain proof)|What is the redemption path — can you actually exit to dollars?|How did it behave during past market stress?|Who can freeze or blacklist your tokens, and under what rules?|Liquidity and acceptance — a stablecoin nobody uses isn't stable in practice"),
   S("The honest bottom line",
     "Every stablecoin makes a trade-off between decentralization, capital efficiency and stability — pick two. Fiat-backed coins dominate because they work, but they import banking-system and regulatory risk. Diversifying across designs is the pragmatic hedge.")],
  ["Stablecoins combine fiat stability with blockchain settlement","Fiat-backed, crypto-backed and algorithmic designs carry different risks","Check the backing, the redemption path, and stress-test history","Diversify across designs — no peg is invulnerable"]),

# ---------------- Developers ----------------
A("solidity-for-beginners","Solidity for Beginners","dev",
  "Your first steps in Ethereum's smart contract language: types, functions, state, and a complete walkthrough of a real contract you can deploy today.",
  "12 min","solidity tutorial beginners smart contract ethereum",
  [S("What Solidity is (and isn't)",
     "Solidity is a statically-typed, contract-oriented language that compiles to EVM bytecode. If you know JavaScript or C++, the syntax will feel familiar — but the mental model is different. Every state change costs gas, code is immutable once deployed, and bugs can burn real money. There is no 'move fast and break things' on mainnet."),
   S("Core concepts in one contract",
     "Every Solidity file declares a license and compiler version, then one or more contracts containing state variables (stored on-chain), functions (which read or modify state), and modifiers (reusable guards like access control).",
     "code"),
   S("The mental model that matters",
     "list:State is expensive — writing to storage is the costliest operation; design to minimize it|Everything is public — 'private' variables are readable by anyone running a node|Calls are transactions — they can fail, revert, and cost gas even when they fail|External calls are dangerous — every call to another contract is a potential reentrancy vector"),
   S("Your learning path from here",
     "Start in the browser with Remix IDE, no setup required. Deploy to a testnet (Sepolia), break things, read other people's contracts on a block explorer. Then graduate to a local framework like Foundry or Hardhat, and finish every project with tests — the testing discipline is what separates hobbyists from professionals.")],
  ["Solidity looks like JS but thinks like a database with money attached","Storage writes, visibility and reentrancy are the big mental shifts","Start in Remix on a testnet — free, fast, consequence-free","Tests and audits are not optional in smart contract development"]),

A("evm-vs-non-evm-chains","EVM vs. Non-EVM Chains","dev",
  "Ethereum's virtual machine became an industry standard — but Solana, Move and Cosmos chose different paths. What the choice means for developers.",
  "9 min","evm non-evm solana move cosmos blockchain architecture",
  [S("What 'EVM-compatible' actually means",
     "The Ethereum Virtual Machine is the runtime that executes Ethereum smart contracts. Dozens of chains — Arbitrum, Polygon, BNB Chain, Avalanche C-Chain — run the same VM. For developers this is powerful: one language (Solidity), one toolchain (Foundry/Hardhat), and code that ports across ecosystems with minimal changes."),
   S("Why some chains said no",
     "list:Solana (Sealevel) — parallel transaction execution and Rust-based programs; raw throughput, steeper learning curve|Move chains (Aptos, Sui) — a resource-oriented language designed to make asset bugs structurally impossible|Cosmos (CosmWasm) — application-specific chains talking over IBC; sovereignty over your whole stack"),
   S("The real trade-offs for builders",
     "EVM chains give you the deepest liquidity, the most users, battle-tested tooling, and a decade of security folklore. Non-EVM chains offer performance headroom and cleaner programming models, but smaller ecosystems, thinner tooling, and fewer auditors who know the stack. Most serious teams prototype on EVM and only go non-EVM when a specific technical requirement demands it."),
   S("A practical decision framework",
     "Choose based on: where your users and liquidity already are, whether your app needs parallel execution or sub-second finality, the availability of senior engineers for the stack, and the maturity of that ecosystem's security tooling. Technology is rarely the deciding factor — distribution is.")],
  ["EVM compatibility means one codebase, many chains","Non-EVM designs trade ecosystem depth for performance or safety","Tooling and auditor maturity are underrated selection criteria","Follow your users and liquidity first, architecture second"]),

A("local-blockchain-dev-environment","Local Blockchain Dev Environment","dev",
  "Set up a professional smart contract development environment from scratch: Foundry, local nodes, forking mainnet, and the workflow pros use.",
  "10 min","foundry hardhat anvil local development environment setup",
  [S("Why local-first development",
     "Deploying to a testnet for every iteration is slow and painful. A local blockchain gives you instant mining, unlimited test ETH, deterministic state, and the ability to fork mainnet — running your contracts against real deployed protocols with real state, entirely offline."),
   S("The toolchain: Foundry",
     "Foundry is the current industry standard: written in Rust, extremely fast, and it lets you write tests in Solidity itself. The suite includes Forge (build & test), Anvil (local node), and Cast (CLI for chain interactions).",
     "code",
     "Alternative: Hardhat remains excellent, especially for TypeScript-heavy teams and its rich plugin ecosystem. The workflow below applies to both."),
   S("The professional workflow",
     "list:forge init — scaffold a project with src/, test/, and a config|anvil — spin up a local node with 10 funded accounts|forge test — run unit tests in milliseconds|anvil --fork-url <RPC> — fork mainnet to test against real protocols|forge script — deterministic, scriptable deployments"),
   S("Habits that pay off immediately",
     "Pin your Solidity version. Write the test before the fix. Fork-test anything that touches an external protocol. And keep a .env discipline — never hardcode keys, never commit secrets, and use separate wallets for development and real funds.")],
  ["Local nodes make iteration instant; forking makes tests realistic","Foundry (Forge/Anvil/Cast) is the modern default toolchain","Fork mainnet whenever your contracts touch external protocols","Key hygiene starts on day one — dev wallets and real wallets never mix"]),

A("gas-optimization-techniques","Gas Optimization Techniques","dev",
  "Cut your contract's gas costs by 30–70% with storage packing, calldata tricks, custom errors and assembly — with the trade-offs honestly labeled.",
  "11 min","gas optimization solidity storage packing evm efficiency",
  [S("Where gas actually goes",
     "Storage writes dominate: a fresh SSTORE costs ~20,000 gas, versus ~100 for memory operations and ~3 for pure arithmetic. The optimization hierarchy is therefore simple — avoid storage, pack what you must store, and make everything else cheap."),
   S("The highest-impact techniques",
     "list:Storage packing — order structs so multiple uint128/bool values share one 32-byte slot|Custom errors — revert with MyError() instead of require strings; saves deployment and runtime gas|calldata over memory — mark external function arrays as calldata to skip copying|unchecked math — skip overflow checks where logic guarantees safety|Immutable & constant — baked into bytecode instead of stored|Cache storage reads — reading the same slot twice costs real money"),
   S("Techniques with honest trade-offs",
     "Assembly (Yul) can cut hot-path costs dramatically but destroys readability and auditability. Bit-packing and compression save gas per call while increasing code complexity and bug surface. Rule of thumb: optimize the functions users call every block, not the ones an admin calls once a year."),
   S("Measure, don't guess",
     "Use forge test --gas-report and snapshots to quantify every change. An 'optimization' that saves 200 gas but doubles audit time is a loss. The best gas optimization is architectural: do less on-chain, batch operations, and push computation off-chain with on-chain verification.")],
  ["Storage is the enemy — writes cost ~100x more than computation","Packing, custom errors and calldata are the safe wins","Assembly is a scalpel, not a hammer — document every line","Profile with gas reports; optimize hot paths only"]),

A("building-your-first-dapp","Building and Deploying Your First DApp","dev",
  "From empty folder to live decentralized application: contract, tests, frontend wallet connection, and a mainnet deployment checklist.",
  "13 min","dapp tutorial deploy frontend web3 wagmi full stack",
  [S("Anatomy of a dApp",
     "A decentralized application has three parts: smart contracts (the backend, living on-chain), a frontend (a normal web app), and a wallet connection layer that lets users sign transactions. The frontend never holds user funds — the wallet does — which is the whole point."),
   S("Step 1 — the contract",
     "Start minimal. A contract with one state variable and two functions teaches you 80% of the workflow. Write it in Solidity, write unit tests covering the happy path and the failure modes, and deploy to a local fork first.",
     "code"),
   S("Step 2 — the frontend",
     "Modern stack: a React app with wagmi + viem for chain interactions and a wallet connector for the connect button. The flow is always the same — connect wallet, read contract state with a call (free), write state with a transaction (costs gas, needs a signature), then listen for the receipt and update the UI."),
   S("Step 3 — deployment checklist",
     "list:Full test coverage on core logic — 90%+ on anything holding funds|Static analysis (Slither) and, for anything serious, an external audit|Deploy to testnet, then do a real user walkthrough with fresh eyes|Verify the contract source on the block explorer|Mainnet deploy from a dedicated deployer wallet, with keys stored properly|Monitor: set up alerts for unusual contract events from day one")],
  ["dApp = contracts + frontend + wallet signing; the frontend never custodies","wagmi/viem make the web3 frontend feel like normal React","Testnet walkthroughs catch what unit tests miss","Deployment is the beginning — monitoring and key security are forever"]),

A("smart-contract-security-vulnerabilities","Smart Contract Security: Top Vulnerabilities","dev",
  "The attack patterns behind crypto's biggest hacks — reentrancy, oracle manipulation, access control failures — and the defenses that actually work.",
  "12 min","smart contract security vulnerabilities reentrancy hacks audit",
  [S("Why smart contract security is different",
     "Deployed code is immutable, contracts hold real money, and attackers can study your bytecode at leisure. There are no patches, no rollbacks (without governance), and exploits execute in a single atomic transaction. Defense must be structural, not reactive."),
   S("The hall of fame",
     "list:Reentrancy — an external call re-enters your function before state updates (The DAO, $60M). Defense: checks-effects-interactions, reentrancy guards|Oracle manipulation — flash-loaned price swings trick your contract into valuing assets wrong. Defense: time-weighted prices, multiple oracle sources|Access control failures — missing onlyOwner on a critical function. Defense: explicit modifiers, role-based systems, test every privileged path|Integer issues — largely solved by Solidity 0.8's built-in checks, but unchecked blocks reintroduce them|Flash loan attacks — not a vulnerability per se, but they weaponize every other bug with unlimited temporary capital"),
   S("The defense stack",
     "list:Write tests that attack your own contract — fuzzing and invariant tests catch what unit tests miss|Run Slither and similar static analyzers in CI|Use battle-tested libraries (OpenZeppelin) instead of rolling your own|Get an external audit for anything holding meaningful value|Consider a bug bounty — cheaper than an exploit|Add circuit breakers: pausable functions and rate limits for the worst case")],
  ["Immutability + money + transparency = security must be structural","Reentrancy and oracle manipulation cause the biggest losses","Checks-effects-interactions and TWAP oracles are table stakes","Layer your defenses: tests, analysis, audits, bounties, breakers"]),

A("layer-2-scaling-explained","Layer 2 Scaling Explained","dev",
  "Optimistic rollups, ZK rollups, validiums — how Layer 2s inherit Ethereum's security while cutting fees 100x, and what it means for your architecture.",
  "10 min","layer 2 rollup optimistic zk arbitrum optimism scaling",
  [S("The scaling trilemma's answer",
     "Ethereum chose decentralization and security over raw throughput — so Layer 2s execute transactions off the main chain, then post compressed proofs or data back to it. Users get near-instant, cent-level transactions; the security of settlement still comes from Ethereum itself."),
   S("The two rollup families",
     "list:Optimistic rollups (Arbitrum, Optimism, Base) — assume transactions are valid, with a 7-day fraud-proof window. EVM-equivalent, mature, but withdrawals to L1 take a week (bridges offer instant exits for a fee)|ZK rollups (zkSync, StarkNet, Polygon zkEVM) — every batch comes with a cryptographic validity proof. Faster finality, no challenge window, but proving is computationally heavy and full EVM equivalence is harder"),
   S("What changes for developers",
     "Mostly, nothing — that is the point. Your Solidity code, Foundry toolchain and contract patterns port directly. The differences that matter: much lower gas means previously uneconomical designs (on-chain games, micro-transactions) become viable; cross-chain messaging replaces some intra-chain calls; and sequencer centralization is a real, if diminishing, consideration."),
   S("Choosing an L2",
     "Evaluate: TVL and ecosystem depth, fraud/validity proof maturity, sequencer decentralization roadmap, data availability design, and bridge security — historically the weakest link, where billions have been lost.")],
  ["L2s execute off-chain and inherit L1 security via proofs","Optimistic = fraud proofs + 7-day window; ZK = validity proofs + fast finality","Existing EVM code ports nearly unchanged","Bridge security is the systemic weak point to understand"]),

A("testing-smart-contracts","Testing Smart Contracts","dev",
  "Unit tests are not enough. Fuzzing, invariant testing, fork testing and formal methods — the full testing pyramid for contracts that hold real money.",
  "10 min","testing smart contracts fuzzing invariant foundry forge",
  [S("Why web2 testing habits fail here",
     "In web2, a bug is a rollback and an apology email. In smart contracts, a bug is a wire transfer to an attacker. Tests must assume an intelligent adversary with unlimited capital (flash loans) and perfect knowledge of your code — because on a public blockchain, they have exactly that."),
   S("The testing pyramid",
     "list:Unit tests — every function, every revert path, every access-control boundary. Baseline: 90%+ coverage on fund-handling code|Fuzz tests — let the framework throw thousands of random inputs at your functions; edge cases you never imagined will surface|Invariant tests — define properties that must ALWAYS hold ('total deposits == contract balance') and let the fuzzer try to violate them through random call sequences|Fork tests — run against real mainnet state to verify integrations with live protocols|Static analysis — Slither in CI catches known patterns automatically"),
   S("Writing invariants that matter",
     "Good invariants express economic truth, not implementation detail: 'no user can withdraw more than they deposited plus yield', 'the sum of balances equals totalSupply', 'a paused contract moves no funds'. When an invariant breaks in fuzzing, you have found a real exploit path — before an attacker does."),
   S("The culture shift",
     "Test-first development is not a luxury in this domain; it is the cost of admission. The time you 'save' skipping fuzzing will be repaid, with interest, either to auditors or to exploiters.")],
  ["Assume an adversary with unlimited capital and your full source code","Fuzzing and invariant tests find what unit tests never will","Fork-test every external protocol integration","Invariants should encode economic truth, not implementation"]),

A("storage-layouts","Storage Layouts","dev",
  "How the EVM actually stores your variables: slots, packing, mappings, and why understanding storage layout is essential for upgrades and gas optimization.",
  "9 min","evm storage layout slots packing upgradeable contracts",
  [S("The 2^256 filing cabinet",
     "EVM storage is a key-value store of 2^256 slots, each 32 bytes wide. State variables are assigned slots in declaration order. Reading a slot costs ~2,100 gas (cold) and writing a fresh slot ~20,000 — which is why storage layout is a financial decision, not just a technical one."),
   S("Packing: your free gas discount",
     "Variables smaller than 32 bytes are packed into a single slot when declared adjacently: a uint128, a uint64 and a bool fit together, turning three storage writes into one. The catch: order matters, and sloppy struct definitions silently waste slots."),
   S("Mappings and dynamic arrays",
     "Mappings don't store keys at all — a value for key k lives at keccak256(k . slot), making collisions astronomically impossible. Dynamic arrays store their length at their slot and elements at keccak256(slot) + i. Understanding this is essential when reading storage directly in assembly or debugging with a node."),
   S("Why upgradeable contracts live and die by layout",
     "Proxy upgrade patterns keep storage in the proxy while swapping the logic contract. Append a variable in the wrong place — or reorder existing ones — and every user's balances silently corrupt. Rules: never reorder, never change types, only append, and use storage gaps in base contracts meant to be inherited.")],
  ["Storage is 2^256 32-byte slots; writes are the priciest EVM operation","Pack small variables adjacently to share slots","Mappings hash their keys — there is no iteration on-chain","Upgrade safety = never reorder storage, only append"]),

A("rpc-reliability","RPC Reliability","dev",
  "Your dApp is only as reliable as its RPC endpoint. Failover strategies, provider trade-offs, rate limits and monitoring for production-grade infrastructure.",
  "8 min","rpc node provider reliability infura alchemy infrastructure",
  [S("The invisible single point of failure",
     "Every read and every transaction your users make flows through an RPC (Remote Procedure Call) endpoint. When it goes down — and they all go down — your beautifully audited contract might as well not exist. Wallets show stale balances, transactions hang, and users blame you, not the provider."),
   S("Provider options and trade-offs",
     "list:Managed providers (Alchemy, Infura, QuickNode) — excellent uptime, dashboards, enhanced APIs; the default for most teams. Risk: centralization and rate limits|Self-hosted nodes — maximum sovereignty, no rate limits, significant ops burden (disk, sync, upgrades)|Decentralized RPC networks — censorship resistance, variable latency, maturing ecosystem"),
   S("The reliability playbook",
     "list:Multi-provider failover — wrap your RPC client so requests fall back across at least two providers automatically|Cache aggressively — block-cached reads (block numbers, historical data) never need to hit the node twice|Respect rate limits — exponential backoff, request batching, and WebSocket subscriptions instead of polling|Monitor from the user's perspective — synthetic transactions and read probes from multiple regions|Have a status page and a degradation plan before you need them"),
   S("The deeper point",
     "Decentralized settlement with a centralized access layer is a compromise the whole industry makes. Architect so that switching providers is a config change, not a rewrite — and keep an eye on the decentralizing infrastructure stack; it is improving fast.")],
  ["RPC is your dApp's lifeline — treat it as critical infrastructure","Multi-provider failover is the minimum bar for production","Cache reads, batch requests, prefer subscriptions over polling","Abstract providers behind a config so switching costs nothing"]),

# ---------------- Tax ----------------
A("crypto-taxes-country-by-country","Crypto Taxes: Country-by-Country Overview","tax",
  "How major jurisdictions tax crypto in 2026: the US, UK, EU, and beyond — taxable events, rates, and reporting regimes compared in one place.",
  "12 min","crypto taxes by country international comparison rates",
  [S("The global pattern (and the exceptions)",
     "Most tax authorities treat crypto as property or an asset, not currency. That means disposal — selling, swapping, spending — is usually a taxable event, and gains are taxed as capital gains or income depending on the jurisdiction and holding period. A few countries remain notably friendly: long-term holdings are tax-free for individuals in Germany (after one year) and Portugal has historically been lenient, though rules evolve constantly."),
   S("Snapshot of major regimes",
     "list:United States — property; short-term gains taxed as ordinary income, long-term at 0/15/20%; crypto-to-crypto swaps are taxable; $600+ broker reporting expanding|United Kingdom — capital gains tax on disposal with a shrinking annual allowance; income tax on mining/staking wages|Germany — tax-free after a 1-year holding period for private sales; under a year taxed as income|EU (general) — varies by member state; DAC8/CARF bring automatic exchange-of-information reporting|Japan — gains taxed as miscellaneous income up to 55%; reform debated|UAE/Singapore — no capital gains tax for individuals (with conditions)"),
   S("The new reporting era",
     "The OECD's Crypto-Asset Reporting Framework (CARF) and the EU's DAC8 directive mean exchanges now automatically share your transaction data with tax authorities across borders. The era of 'they'll never know' is definitively over — compliance is the only strategy."),
   S("Practical universal advice",
     "list:Keep records of every trade, swap and transfer — date, amount, value in fiat|Track cost basis from day one, not at tax time|Treat airdrops, staking rewards and mining as income on receipt in most jurisdictions|Use reputable tax software or a crypto-savvy accountant|When in doubt, disclose — penalties for evasion dwarf the tax itself")],
  ["Most countries tax crypto as property: disposal = taxable event","Holding-period exemptions (e.g. Germany) reward patience","CARF/DAC8 mean automatic cross-border reporting is here","Records and disclosure beat cleverness every time"]),

A("how-to-calculate-capital-gains","How to Calculate Capital Gains on Crypto Trades","tax",
  "Cost basis, proceeds, holding periods — a worked-example guide to calculating crypto capital gains correctly, including the mistakes that trigger audits.",
  "9 min","capital gains calculation cost basis crypto tax",
  [S("The core formula",
     "Capital gain or loss = proceeds (what you received) minus cost basis (what you paid, including fees). Buy 1 ETH for $2,000 with $10 in fees and your basis is $2,010. Sell for $3,000 and your gain is $990. Everything else is detail — but the detail is where people get burned."),
   S("What counts as a taxable disposal",
     "list:Selling crypto for fiat|Swapping one crypto for another (yes, ETH→USDC is taxable in most jurisdictions)|Spending crypto on goods or services|Gifting (in some jurisdictions, above thresholds)|NOT usually taxable: buying with fiat, transferring between your own wallets, holding"),
   S("A worked example with multiple lots",
     "You bought 0.5 ETH at $1,800 in January and 0.5 ETH at $2,400 in June. In December you sell 0.5 ETH for $3,000. Which lot did you sell? Under FIFO it's the January lot: gain = $3,000 − $1,800 = $1,200. Under specific identification (where allowed), you could choose the June lot: gain = $600. The method you choose — and must apply consistently — changes your bill materially."),
   S("Mistakes that trigger audits",
     "list:Forgetting crypto-to-crypto swaps are taxable disposals|Using the exchange's year-end summary without cross-checking your own wallets|Ignoring fees in basis calculations (they add up)|Missing the holding-period boundary that changes your rate|Assuming losses offset everything without checking local wash-sale or matching rules")],
  ["Gain = proceeds − cost basis (fees included in basis)","Swaps and spending are disposals, not just sales","Lot selection method (FIFO vs specific ID) changes your bill","Reconcile exchanges AND personal wallets before filing"]),

A("crypto-tax-software-compared","Crypto Tax Software Compared","tax",
  "The leading crypto tax platforms head-to-head: exchange coverage, DeFi support, accuracy and pricing — plus when software isn't enough.",
  "10 min","crypto tax software comparison koinly coinledger review",
  [S("What good crypto tax software must do",
     "The job sounds simple — aggregate transactions, compute gains, produce forms — but DeFi broke the simple case years ago. The differentiators today: automatic wallet/exchange sync coverage, correct handling of DeFi (LP positions, staking, bridges), cost-basis method support for your jurisdiction, and an auditable trail you could defend."),
   S("The evaluation checklist",
     "list:Integrations — does it natively support YOUR exchanges, chains and wallets?|DeFi depth — can it correctly classify LP adds/removes, staking rewards, and wrapped tokens?|Cost basis methods — FIFO, LIFO, HIFO, specific ID, and country-specific rules|Error handling — how does it surface unmatched transactions (the accuracy killer)?|Output — country-specific forms and reports, accountant export|Price — tiers usually scale with transaction count; heavy DeFi users need higher tiers"),
   S("Accuracy: where software falls down",
     "Every platform struggles with the same edge cases: tokens received from contracts it doesn't recognize (labeled 'unknown'), bridged assets appearing as disposals, and spam airdrops inflating income. Budget time to review flagged transactions manually — the software proposes, you dispose."),
   S("When you need a human",
     "If you have six-figure DeFi activity, cross-border residency changes, business income in crypto, or prior-year amendments, software is a data-prep tool for a professional — not the final answer. The fee for a crypto-literate accountant is cheap insurance at that scale.")],
  ["DeFi handling quality separates serious tools from simple aggregators","Review unmatched and flagged transactions manually — always","Match the tool's cost-basis methods to your jurisdiction","Large or complex activity = software + professional, not either/or"]),

A("defi-taxes-staking-yield-airdrops","DeFi Taxes: Staking, Yield, and Airdrops","tax",
  "When is staking income taxable? What about LP rewards and airdrops? The current treatment of DeFi's trickiest income types, explained plainly.",
  "10 min","defi taxes staking rewards airdrop income taxable",
  [S("The two-moment principle",
     "Most jurisdictions apply a two-moment rule to DeFi income: you owe income tax when you RECEIVE tokens (at their fair market value that day), and capital gains tax later when you DISPOSE of them (gain = sale price minus the value already taxed). Miss the first moment and you're under-reporting; double-count it and you're overpaying."),
   S("Staking rewards",
     "The prevailing treatment: staking rewards are income on receipt, valued at market price when they hit your wallet (or when you gain dominion and control). When you later sell, only the appreciation since receipt is a capital gain. Some jurisdictions debate taxing staking only at sale — know your local position, and document either way."),
   S("Liquidity pool and farming rewards",
     "list:Adding/removing liquidity — often treated as a disposal (swapping tokens for LP tokens), though treatment varies|Farming incentives (governance tokens etc.) — income on receipt at fair market value|Fees earned inside a pool — realized when you withdraw; tracking the split between principal and reward is the hard part|Impermanent loss — generally NOT a deductible loss until you actually withdraw and dispose"),
   S("Airdrops and hard forks",
     "Typically income on receipt at fair market value — including the unpleasant case where you receive tokens, owe tax on their value, and then they crash. Worthless spam airdrops generally have zero value at receipt, but document your reasoning."),
   S("The recordkeeping reality",
     "DeFi income can mean thousands of micro-events per year. Automated tracking is not optional; neither is choosing one consistent valuation source (a reputable price oracle) and sticking with it.")],
  ["Two tax moments: income at receipt, capital gains at disposal","Staking and farming rewards are income at fair market value on receipt","IL isn't a deductible loss until realized on withdrawal","Automate tracking — DeFi event volume defeats manual records"]),

A("nft-taxation-guide","NFT Taxation Guide","tax",
  "Buying, selling, minting, and earning royalties — how NFTs are taxed for collectors, traders and creators, with the gray areas flagged honestly.",
  "9 min","nft taxes royalties mint collectibles capital gains",
  [S("NFTs are taxable assets, not magic exceptions",
     "Tax authorities treat NFTs like other crypto assets: disposal triggers capital gains, and creation income is income. The wrinkles: buying an NFT with crypto is itself a disposal of that crypto (two taxable events in one click), and some jurisdictions apply higher 'collectibles' rates to NFT gains."),
   S("For collectors and traders",
     "list:Minting — gas fees add to your cost basis; the crypto spent is a disposal|Buying on secondary — same: basis includes price + fees; the ETH/SOL spent is a taxable disposal|Selling — capital gain or loss against your basis; watch for collectibles rates|Airdropped NFTs — typically income at fair market value on receipt|Wash trading your own NFTs — tax fraud in most jurisdictions, and marketplaces report data"),
   S("For creators",
     "Mint-and-sell revenue and ongoing royalties are ordinary income (or business income if you're operating as one) at the value when received. Creators should track: income on each sale/royalty, basis for later disposal of unsold inventory, and deductible expenses (tools, gas, contractors)."),
   S("Gray areas to discuss with a professional",
     "Fractionalized NFTs (security or collectible?), NFTs as loan collateral (disposal or not?), and gaming assets earned through play (income on receipt, or on cash-out?). Guidance here is evolving — document your positions and their rationale.")],
  ["Buying an NFT with crypto is TWO taxable events","Creators owe income tax on primary sales and royalties when received","Collectibles tax rates may be higher than standard capital gains","Fractionalization and collateralization remain gray — get advice"]),

A("crypto-tax-loss-harvesting","Crypto Tax-Loss Harvesting","tax",
  "Turn your losing positions into tax savings: how loss harvesting works for crypto, the wash-sale question, and a step-by-step year-end playbook.",
  "8 min","tax loss harvesting wash sale crypto losses offset",
  [S("The opportunity in red positions",
     "Capital losses offset capital gains — and in many jurisdictions, a limited amount of ordinary income too, with the rest carried forward. Crypto's volatility makes this powerful: positions underwater by December can be sold to crystallize a loss that shelters your winners, potentially saving you thousands."),
   S("The wash-sale question",
     "In traditional securities, selling at a loss and rebuying within 30 days disallows the loss (the wash-sale rule). In several jurisdictions — notably, historically, the US — crypto's property classification has meant wash-sale rules did not apply, allowing sell-and-immediately-rebuy strategies. This loophole has been repeatedly targeted by legislation; verify the current rules in your jurisdiction before relying on it."),
   S("The year-end playbook",
     "list:1. Run a gains report in October/November — know your net position early|2. Identify losers you genuinely want to exit — don't let the tax tail wag the investment dog|3. Sell before year-end to crystallize; document timestamps and values|4. If rebuying, understand your jurisdiction's wash-sale/matching rules first|5. Offset short-term against short-term first where rates differ|6. Carry forward unused losses properly — they don't expire in many regimes"),
   S("Mistakes to avoid",
     "Harvesting a loss on an asset you immediately rebuy without checking wash-sale rules, forgetting that transfers between your own wallets realize nothing (only disposals do), and harvesting so aggressively that you exit positions you believed in for a tax benefit worth less than the upside you abandoned.")],
  ["Realized losses offset gains — and sometimes limited ordinary income","Wash-sale rules for crypto vary and are changing; verify locally","Start the analysis in Q4, not the week before filing","Harvest strategically — never let tax drive bad investment exits"]),

A("how-exchanges-report-to-tax-authorities","How Exchanges Report Your Activity to Tax Authorities","tax",
  "Think your exchange activity is private? Here's exactly what platforms report, to whom, and how the new global reporting frameworks close the gaps.",
  "8 min","exchange reporting tax authorities carf dac8 1099",
  [S("What exchanges already report",
     "Centralized exchanges are regulated businesses. They collect KYC (your identity), and they share data: directly to tax authorities via required information returns, automatically under international agreements, and on demand through legal process. Major exchanges have handed over user records in bulk under court orders more than once."),
   S("The new global machinery",
     "list:CARF (OECD) — Crypto-Asset Reporting Framework: automatic exchange of crypto transaction data between dozens of participating countries|DAC8 (EU) — the EU directive implementing CARF, binding on all member states' crypto service providers|Broker reporting (US) — expanding requirements for exchanges and, contentiously, some DeFi front-ends to issue tax forms|Travel rule — identity data attached to transfers above thresholds between regulated platforms"),
   S("What this means in practice",
     "Your exchange account is effectively transparent to your tax authority: balances, trades, and increasingly transfers to external wallets. Moving coins to a self-custody wallet is legal and private on-chain — but the exchange's record of the withdrawal links your identity to that address. Authorities increasingly use blockchain analytics to follow the trail."),
   S("The rational response",
     "Compliance. Report accurately, keep your own records (exchanges shut down and data disappears), and reconcile what you file against what exchanges will report. The cost of honest filing is the tax. The cost of being caught otherwise is the tax, plus penalties, plus interest, plus — in egregious cases — prosecution.")],
  ["Exchanges share your data via returns, treaties and court orders","CARF/DAC8 make cross-border automatic reporting the norm","Withdrawals to self-custody link your identity to that address","Reconcile your filing against what platforms report — they will"]),

A("crypto-compliance-for-startups","Crypto Compliance for Startups","tax",
  "Building a crypto company? The compliance foundations you need before launch: licensing, AML/KYC, tax infrastructure and the mistakes that kill startups.",
  "11 min","crypto startup compliance aml kyc licensing regulation",
  [S("Compliance is a launch requirement, not a later problem",
     "The most common fatal startup mistake in crypto: treating compliance as something to add after product-market fit. Regulators disagree, retroactively. Teams have faced enforcement for activities years old, and banking partners, investors and acquirers all conduct compliance due diligence. Build the skeleton before you need it."),
   S("The foundational questions",
     "list:Are you a money transmitter / VASP? — custody or exchange of customer funds usually triggers licensing|What jurisdictions do you serve? — 'we're decentralized' is not a jurisdiction strategy|Do you touch securities? — token design can create securities-law exposure|What's your AML/KYC posture? �� even non-custodial products face sanctions-screening expectations for front-ends|How will you handle taxes? — your entity's crypto treasury, token compensation, and revenue all need infrastructure"),
   S("The minimum viable compliance stack",
     "list:Legal opinion on your token/activity classification in target markets|Entity structure that matches your regulatory footprint|AML policy + sanctions screening tooling from day one of handling funds|Accounting stack that handles crypto natively (subledger + tax engine)|Record-retention discipline — assume every decision will be reviewed in 3 years"),
   S("Budget and sequencing reality",
     "Serious licensing (e.g., US state MTLs, EU MiCA CASP authorization) takes 6–18 months and six-to-seven figures. Many startups therefore launch in permissive jurisdictions with restricted access, or design non-custodial products that reduce licensing scope. Both are legitimate strategies — pretending regulation doesn't apply to you is not.")],
  ["Retroactive enforcement makes 'comply later' a existential gamble","Custody and exchange of funds trigger licensing almost everywhere","Token design, AML and tax infrastructure are day-one decisions","Licensing timelines shape go-to-market — plan for 6–18 months"]),

A("cost-basis-methods","Cost Basis Methods","tax",
  "FIFO, LIFO, HIFO, specific identification — how your choice of accounting method changes your crypto tax bill, with worked numbers.",
  "8 min","cost basis fifo lifo hifo specific identification accounting",
  [S("Why the method matters",
     "When you sell part of a position bought at different times and prices, which units did you sell? The answer — your cost basis method — determines your gain. Across many trades and years, the difference between methods can be tens of thousands of dollars on the same transaction history."),
   S("The methods, with numbers",
     "You bought: 1 BTC at $30,000 (lot A), 1 BTC at $50,000 (lot B), 1 BTC at $70,000 (lot C). You sell 1 BTC at $80,000.",
     "list:FIFO (first in, first out) — sells lot A: gain = $50,000|LIFO (last in, first out) — sells lot C: gain = $10,000|HIFO (highest in, first out) — sells lot C: gain = $10,000|Specific ID — you designate the lot at sale: your choice, if your records prove it"),
   S("Rules that constrain you",
     "list:Jurisdiction — some countries mandate FIFO or average cost; others allow choice|Consistency — switching methods opportunistically year to year invites scrutiny|Specific ID requires contemporaneous records — you must be able to prove which units moved, on-chain where possible|Long-term vs short-term — the method also determines holding period, which changes rates in many countries"),
   S("Practical guidance",
     "HIFO generally minimizes current-year tax (highest basis first), FIFO often maximizes long-term rates (oldest lots first) — the 'best' method depends on your rates and horizon. Choose deliberately, apply consistently, and let good software track it across wallets.")],
  ["Your basis method determines both gain size and holding period","HIFO minimizes current gains; FIFO often optimizes long-term rates","Jurisdictions may mandate a method — check before choosing","Specific ID is powerful but demands provable, contemporaneous records"]),

A("wallet-recordkeeping","Wallet Recordkeeping","tax",
  "The recordkeeping system that makes crypto taxes painless: what to track, how to structure it, and the habits that survive an audit.",
  "7 min","wallet recordkeeping transaction records audit trail",
  [S("Why your future self needs this",
     "Tax authorities can ask for records years after the fact. Exchanges shut down, wallets get replaced, chains get abandoned — and 'I can't reconstruct it' is not a defense. A lightweight system built now saves weeks of forensic accounting later."),
   S("What to record for every transaction",
     "list:Date and time (with timezone)|Asset, amount, and the counter-asset or fiat value at the time|Type: buy, sell, swap, transfer, income, gift, fee|Wallet addresses involved (yours, labeled)|Transaction hash — the permanent on-chain receipt|Purpose — one line: 'swapped ETH to USDC to take profit' beats guessing in 2029"),
   S("The system that works",
     "list:Label your wallets NOW — 'Ledger vault', 'MetaMask DeFi', 'exchange hot wallet' — so transfers between them are never confused with disposals|Export CSVs from every exchange quarterly — platforms limit history windows|Snapshot year-end balances per wallet — the reconciliation anchor|One source of truth — a tax platform or spreadsheet where everything converges|Back it up — records deserve the same redundancy as your seed phrase"),
   S("The audit-survival test",
     "For any number on your tax return, you should be able to produce: the transaction hash or exchange record, the valuation source, and the basis calculation. If a stranger with your records could rebuild your return without asking you a question, you pass.")],
  ["Record every transaction's hash, value, type and purpose","Label wallets and export exchange data on a schedule","Year-end balance snapshots anchor reconciliation","Pass the stranger test: records must rebuild your return unaided"]),

# ---------------- Gaming ----------------
A("what-is-web3-gaming","What Is Web3 Gaming?","gaming",
  "Beyond the buzzwords: what blockchain actually adds to games, where the industry is after the hype cycle, and what matters for players and builders.",
  "9 min","web3 gaming blockchain games explained ownership",
  [S("The one-sentence version",
     "Web3 gaming puts game assets — items, characters, currencies — on a blockchain as tokens you actually own, in your wallet, independent of any single game's servers. The promise: your sword survives the game's shutdown, and your hours of grinding become property, not just a database row the studio can delete."),
   S("What blockchain genuinely adds",
     "list:True ownership — assets are yours; tradeable on open markets without permission|Portability (aspirational) — the dream of items moving between games, technically possible, practically rare|Player economies — real markets with real prices, for better and worse|Provable scarcity — on-chain supply anyone can verify|Composability — third parties can build tools and experiences around a game's assets"),
   S("What it doesn't fix",
     "Blockchain doesn't make a bad game fun. The 2021–2022 play-to-earn wave proved that financialization without gameplay collapses the moment new-player inflows slow. The survivors of that crash share a trait: the game is worth playing with zero earnings, and the economy is a bonus, not the product."),
   S("Where the industry is now",
     "Post-hype, the space is quietly maturing: better-funded studios, 'web2.5' designs that hide wallets entirely behind familiar UX, and a focus on ownership as a feature rather than a pitch. The next wave wins on gameplay first — the chain is infrastructure, not marketing.")],
  ["Web3 gaming = player-owned assets on open rails","Ownership and open economies are real; portability is still aspirational","Play-to-earn collapsed because earnings can't substitute for fun","The winning formula: great game first, blockchain underneath"]),

A("play-to-earn-explained","Play-to-Earn Explained","gaming",
  "The rise and crash of play-to-earn, the economics that doomed most of it, and the sustainable models replacing it.",
  "8 min","play to earn p2e game economy axie tokenomics",
  [S("The model that minted and broke an industry",
     "Play-to-earn (P2E) paid players real, tradeable tokens for gameplay. At its peak, top players in developing countries earned above local wages — a genuinely remarkable moment. Then the math caught up: rewards were paid in inflationary tokens, sustained only by new players buying in. When growth slowed, token prices collapsed, earnings evaporated, and the exodus accelerated the crash. Classic reflexivity."),
   S("Why most P2E economies failed",
     "list:Emissions without sinks — tokens printed for playing, with nothing compelling to spend them on|Mercenary capital — players were yield farmers with game clients; they left the moment APR dropped|Ponzi dynamics — early players' earnings were late players' deposits, structurally|No fun moat — when earning stopped, there was no reason to stay"),
   S("The sustainable successors",
     "list:Play-and-own — ownership of assets without promised yields; value comes from utility and scarcity|Cosmetic economies — Counter-Strike proved for a decade that players pay for status, not salary|Skill-based wagering & prizes — players fund the prize pools, not inflation|Sinks by design — crafting, breeding, upgrades that burn tokens because players WANT the result"),
   S("The investor's filter",
     "Ask of any 'earning' game: where does the money players withdraw come from? If the honest answer is 'other players' deposits or token emissions', you are looking at a timer, not a business.")],
  ["P2E collapsed because emissions need endless new demand","Fun is the only durable sink; salary gameplay attracts only farmers","Play-and-own and cosmetic economies are the sustainable heirs","Follow the money out: if it's other players' deposits, it's a timer"]),

A("nft-utility-beyond-art","NFT Utility Beyond Art","gaming",
  "NFTs as access keys, identity, licenses and game assets — the use cases that survive the art-market cycle.",
  "8 min","nft utility access membership identity use cases",
  [S("Art was the demo, not the product",
     "Profile-picture NFTs introduced the world to verifiable digital ownership, but the technology is a primitive: a unique, ownable, programmable token. The durable use cases treat NFTs as infrastructure — keys, credentials and licenses — rather than collectibles."),
   S("Utility that's working now",
     "list:Access & membership — token-gated communities, events and content; the NFT is the pass|In-game assets — items and characters players truly own and can trade|Licensing & IP — commercial rights bundled with the token|Identity & credentials — soulbound-style tokens for achievements, attendance, reputation|Ticketing — verifiable, transferrable, scalper-resistant admission"),
   S("Evaluating utility claims",
     "The test is brutal and simple: does this NEED to be an NFT? Utility that works only inside one company's database gains nothing from a blockchain. Utility that requires ownership verification across independent parties — resale royalties, cross-platform access, open trading — is where the technology earns its complexity."),
   S("Red flags in 'utility' projects",
     "Roadmaps where utility is perpetually 'coming', perks that depend entirely on the founding team's continued enthusiasm, and 'staking rewards' that are just token emissions wearing a utility costume. Real utility works on day one or has a binding reason it can't.")],
  ["NFTs are a primitive: unique, ownable, programmable tokens","Access, game assets, licensing and identity are working use cases","The filter: does this need cross-platform verifiable ownership?","Perpetual-roadmap utility is usually no utility"]),

A("game-studios-blockchain-integration","How Game Studios Are Integrating Blockchain","gaming",
  "From AAA experiments to indie innovation: the actual integration patterns studios use, why most assets stay off-chain, and the 'web2.5' playbook.",
  "9 min","game studios blockchain integration web2.5 development",
  [S("The integration spectrum",
     "Studios integrate blockchain at wildly different depths: (1) cosmetic — a marketplace for a handful of tradeable items; (2) economic — in-game currency on-chain; (3) asset-native — all items are NFTs; (4) fully on-chain — game logic itself runs in smart contracts. Almost all commercial projects sit at levels 1–2, and the reasons are instructive."),
   S("Why most of the game stays off-chain",
     "list:Performance — blockchains process thousands of times fewer operations than game servers need|Cost — on-chain state is the most expensive database in the world|Iteration — games need patches; immutable contracts resist them|UX — players will not sign a transaction per action"),
   S("The web2.5 playbook that works",
     "list:Abstract the wallet — embedded wallets created silently at signup; no seed phrases for players|Gas sponsorship — the studio pays transaction fees; players never see gas|Custodial on-ramps — start custodial for frictionless onboarding, offer self-custody withdrawal for power users|Off-chain gameplay, on-chain settlement — the game server runs the game; the chain records ownership"),
   S("Lessons from the field",
     "Announce blockchain features to your existing community carefully — several studios faced severe backlash from players who associate NFTs with scams. The studios succeeding lead with the benefit (tradeable items, real ownership) and keep the technology invisible. Players adopt features, not protocols.")],
  ["Most commercial games put only ownership settlement on-chain","Performance, cost and iteration keep game logic off-chain","Embedded wallets and gas sponsorship are the UX unlock","Sell the benefit to players; never lead with the technology"]),

A("best-wallets-for-web3-gaming","Best Wallets for Web3 Gaming","gaming",
  "Session keys, embedded wallets, hardware options — choosing the right wallet setup for blockchain gaming, whether you're a player or a whale collector.",
  "8 min","gaming wallets session keys embedded wallet comparison",
  [S("Gaming changes the wallet requirements",
     "A DeFi user signs a few high-stakes transactions. A gamer might trigger hundreds of micro-interactions per session. The wallet stack that works for gaming therefore optimizes for: zero-friction signing, mobile support, and security isolation — your game wallet should never be your life-savings wallet."),
   S("The three setups",
     "list:Embedded wallets — created invisibly inside the game (email/social login); best onboarding, custodial trade-off|Browser/mobile hot wallets — MetaMask, Phantom et al. with gaming-friendly chains; the flexible default|Smart wallets with session keys — approve a limited, time-boxed key that signs small in-game actions without popups; the emerging gold standard"),
   S("What to look for",
     "list:Session key support — no popup per action|Chain coverage — gaming lives on specific chains (Ronin, Immutable, Polygon, Solana)|NFT display and management that doesn't feel like an afterthought|Hardware-wallet compatibility for your valuable assets|A clean separation story — easy multi-account management"),
   S("The security architecture that saves you",
     "Three tiers: a hot 'play' wallet holding only this week's gaming budget and common items; a smart wallet or hardware-secured wallet for valuable assets; and iron discipline about signatures — malicious 'free mint' sites target gamers specifically because gaming normalizes frequent signing. Read every signature request; revoke approvals monthly.")],
  ["Gaming wallets optimize for frictionless signing, not just custody","Session keys eliminate per-action popups safely","Separate play funds from valuable assets — always","Frequent signing makes gamers prime phishing targets — stay sharp"]),

A("economics-of-ingame-nft-marketplaces","The Economics of In-Game NFT Marketplaces","gaming",
  "Royalties, fees, price discovery and liquidity: how player-owned marketplaces actually make money, and what healthy economy design looks like.",
  "9 min","nft marketplace economics royalties game economy fees",
  [S("The business model shift",
     "Traditional games monetize the primary sale and shut down gray markets. Web3 games monetize every trade forever: marketplace fees (typically 1–5%) plus creator royalties (historically 2.5–10%, though enforceability has eroded). Done right, a healthy player economy can out-earn the game's initial sales."),
   S("The liquidity problem",
     "Most game NFTs are horrifically illiquid: unique items, niche demand, thin order books. Prices are set by the last marginal trade, and 'floor price' is a fiction for anything beyond the most common items. Markets that work — aggregated marketplaces, AMM-style pools for fungible-ish items, rental markets for utility assets — all attack this liquidity problem."),
   S("Design levers for a healthy economy",
     "list:Sinks before sources — items must be consumed, upgraded, or burned at rates that absorb supply|Tiered scarcity — abundant commons for accessibility, genuine rarity for status|Utility-anchored pricing — items worth buying to USE, not only to flip|Fee sustainability — royalties that fund ongoing development without choking trade volume|Bot and wash-trading resistance — fake volume kills real price discovery"),
   S("Reading a marketplace's health",
     "Look past floor price: unique buyer count, ratio of listings to holders, volume from unique wallets (not circular trades), and whether top items sell near their asking prices. A healthy marketplace shows diverse participants trading utility; a dying one shows the same wallets passing items in circles.")],
  ["Fees + royalties turn every trade into studio revenue","Illiquidity is the core problem; aggregation and rentals are the fixes","Sinks must absorb supply or prices trend to zero","Judge health by unique participants, not floor price"]),

A("web3-gaming-scams-rug-pulls","Web3 Gaming Scams: Rug Pulls","gaming",
  "Fake mints, malicious signatures, vaporware studios — the scam patterns targeting gamers, and the due diligence that protects you.",
  "9 min","web3 gaming scams rug pull fake mint phishing",
  [S("Why gamers are prime targets",
     "Gaming normalizes exactly the behaviors scammers exploit: clicking mint links fast (FOMO), signing frequent transactions (session fatigue), and trusting community hype (guilds, Discords, influencers). Add younger, less security-experienced users, and web3 gaming is a target-rich environment."),
   S("The greatest hits",
     "list:The vaporware rug — cinematic trailer, token sale, 'game' that never ships; founders drift away with the raise|Fake mint sites — clones of legitimate projects promoted through hacked Twitter/Discord accounts; the 'mint' transaction drains your wallet|Malicious signature requests — setApprovalForAll disguised as a mint, granting the attacker your entire NFT collection|Honeypot tokens — game tokens you can buy but never sell|Pig-butchering guilds — 'scholarship managers' who are really running Ponzi recruitment"),
   S("Ten minutes of due diligence",
     "list:Team — doxxed, verifiable track record, or at least long public history?|Playable anything — a build, a demo, real gameplay footage (not cinematic renders)?|Contract check — verified source, sane permissions, no mint-to-infinity functions?|Token allocation — what percentage can insiders dump, and when?|Community quality — real discussion, or bots echoing rocket emojis?"),
   S("The iron rules",
     "Never sign setApprovalForAll for a mint. Verify URLs obsessively — bookmark, don't click. Use a burner wallet for every new mint. And remember: if a game needs you to recruit others to profit, you are not the player — you are the product.")],
  ["Gamers' FOMO and signature habits are the attack surface","setApprovalForAll on a mint = handing over your whole collection","Doxxed teams, playable builds and sane contracts are the baseline","Burner wallets for every new project — no exceptions"]),

A("interoperability-in-web3-games","Interoperability in Web3 Games","gaming",
  "The dream of items that move between games: what's technically possible today, why it barely happens, and the designs inching toward it.",
  "8 min","interoperability cross game assets metaverse standards",
  [S("The promise vs. the present",
     "The pitch was intoxicating: your sword from Game A becomes your skin in Game B. The reality, years in: almost nothing works this way. Not because the blockchain can't do it — the token is portable by design — but because games are closed artistic and economic systems, and importing foreign assets is usually against the developer's interests."),
   S("Why it mostly doesn't happen",
     "list:Art pipelines — a 3D asset from one game doesn't fit another's engine, style or rig|Balance — an overpowered imported item destroys game economies|Incentives — studios want you buying THEIR items, not arriving with someone else's|IP and licensing — whose lawyer approves Spider-Man swinging through a rival's world?"),
   S("What's actually working",
     "list:Shared-universe ecosystems — one company builds multiple games around one asset set (the realistic path)|Identity and achievements — cross-game reputation and profiles, no asset translation needed|Marketplace interoperability — the same assets tradeable across many third-party marketplaces (this genuinely works)|Composable standards — token standards designed so third parties can build experiences around assets without the studio's permission"),
   S("Where it goes from here",
     "Expect interoperability at the ecosystem layer (one studio, many games) and the infrastructure layer (wallets, identity, marketplaces) long before the fantasy of arbitrary cross-game items. The open-metaverse vision survives — but as composability around assets, not asset teleportation.")],
  ["Token portability is solved; game integration is the real barrier","Art, balance and incentive mismatches block cross-game items","Shared-universe ecosystems are the working form of interoperability","Watch identity and marketplace layers — that's where it's real"]),

A("nft-utility-beyond-hype","NFT Utility Beyond the Hype","gaming",
  "A clear-eyed audit of which NFT utilities retained value through the bear market — and which were always marketing.",
  "7 min","nft utility value bear market audit real use",
  [S("The bear market as audit",
     "When speculation drained out of NFT markets, utilities separated into two piles: those people kept using when there was no money to be made, and those abandoned the moment flipping stopped being profitable. That natural experiment is the most honest data the industry has produced."),
   S("Utility that survived",
     "list:Membership with real community — access people would pay for in any technology|Game assets in games people actually play — utility anchored to fun|Art collected as art — the honest version of the original use case|Ticketing and access passes — where verification solves a real problem (fraud, scalping)"),
   S("Utility that evaporated",
     "list:'Future metaverse' promises — perpetual roadmaps with no shipping dates|Token-gated content behind NFTs nobody wanted for the content itself|Staking-for-rewards — emissions dressed as utility|Celebrity and brand cash-grabs with no ongoing commitment"),
   S("The durable framework",
     "Ask three questions of any utility: Would someone pay for this benefit with plain money? Does the benefit exist independent of the NFT's resale value? Is the issuer structurally committed (revenue model, reputation, legal obligation) to maintaining it? Three yeses and you may have something real. Anything less is a bet on the greater fool.")],
  ["The bear market audited utility better than any analyst","Survivors: membership, played games, honest art, ticketing","'Future utility' with no shipping date is not utility","Would you pay cash for this perk? Start there"]),

A("player-owned-assets","Player-Owned Assets","gaming",
  "What 'owning' a game asset legally and technically means, the gap between marketing and reality, and how to evaluate ownership claims.",
  "8 min","player owned assets digital ownership nfts rights",
  [S("What ownership actually includes",
     "Owning a game asset NFT means the token is in your wallet and no one — not even the studio — can seize or delete it from the chain. What it usually does NOT include: the underlying art's copyright, any guarantee the game will keep rendering or supporting the asset, or protection against the studio releasing ten thousand more of your 'rare' item."),
   S("The layers of an ownership claim",
     "list:Token layer — the NFT itself: genuinely yours, transferable, seizure-resistant|Asset layer — the art/metadata: often hosted on company servers or IPFS; check what happens if the studio disappears|Game layer — the item's function: entirely dependent on the studio's servers and goodwill|Legal layer — the license: read it; most grant display rights, some grant commercial rights, a few grant nothing"),
   S("Evaluating real vs. theatrical ownership",
     "list:Is metadata on-chain or on decentralized storage — or on the studio's API?|Is supply capped by contract, or by a tweet promising not to mint more?|Can the contract be upgraded to change your item's properties?|Does the license give you anything beyond 'look at it'?|If the studio vanished tomorrow, what exactly would you still have?"),
   S("The balanced verdict",
     "Player ownership is real progress — open secondary markets, censorship-resistant holdings, and exit liquidity the old model never offered. But 'own your assets' marketing routinely overstates the legal and practical bundle you're buying. Own with open eyes: the token is yours; the experience around it is rented.")],
  ["You own the token; art, function and license are separate layers","Metadata location and supply caps reveal true ownership depth","Read the license — display rights ≠ commercial rights","Ownership of the token is real; the experience is rented"]),

]

assert len(ARTICLES) == 40, len(ARTICLES)

DATES = ["2026-08-{}".format(str(3 + i * 2 % 27).zfill(2)) for i in range(len(ARTICLES))]

# ---------------------------------------------------------------- helpers
def esc(s): return s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")

def author_url(author_key):
    return f"/authors/{AUTHORS[author_key]['slug']}/"

def seo_head(path, title, desc, breadcrumbs, article=None, profile=None):
    canonical = "https://cryptostackhub.com" + (path if path.endswith("/") or path == "/" else path + "/")
    image = "https://hebbkx1anhila5yf.public.blob.vercel-storage.com/IMAGE1-YZ0juMeTaU0SKgH2ReCpoWiDNaZzMo.png" if article and article["slug"] == "what-is-defi" else "https://cryptostackhub.com/assets/images/og-default.png"
    crumbs_json = []
    for label, url in breadcrumbs:
        item_url = "https://cryptostackhub.com" + (url if url.endswith("/") or url == "/" else url + "/")
        crumbs_json.append({"@type":"ListItem","position":len(crumbs_json)+1,"name":label,"item":item_url})
    graph = [
        {"@type":"Organization","@id":"https://cryptostackhub.com/#organization","name":"CryptoStackHub","url":"https://cryptostackhub.com/","logo":{"@type":"ImageObject","url":"https://cryptostackhub.com/assets/images/cryptostackhub-logo.png"},"image":image},
        {"@type":"BreadcrumbList","@id":canonical+"#breadcrumb","itemListElement":crumbs_json}
    ]
    if profile:
        graph.append({"@type":"Person","@id":"https://cryptostackhub.com"+author_url(profile)+"#person","name":AUTHORS[profile]["name"],"jobTitle":AUTHORS[profile]["role"],"description":AUTHORS[profile]["bio"],"url":"https://cryptostackhub.com"+author_url(profile),"worksFor":{"@id":"https://cryptostackhub.com/#organization"}})
    if article:
        author = AUTHORS[article["author_key"]]
        graph.append({"@type":"Article","@id":canonical+"#article","mainEntityOfPage":{"@type":"WebPage","@id":canonical},"headline":article["title"],"description":article["desc"],"datePublished":article["date"],"dateModified":article.get("dateModified",article["date"]),"author":{"@type":"Organization","@id":"https://cryptostackhub.com"+author_url(article["author_key"])+"#organization","name":author["name"],"url":"https://cryptostackhub.com"+author_url(article["author_key"])},"publisher":{"@id":"https://cryptostackhub.com/#organization"},"image":[image]})
    schema = '<script type="application/ld+json">' + json.dumps({"@context":"https://schema.org","@graph":graph},ensure_ascii=False,separators=(",",":")) + '</script>'
    og_type = "article" if article else "website"
    return f'''
<link rel="canonical" href="{canonical}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:type" content="{og_type}">
<meta property="og:url" content="{canonical}">
<meta property="og:site_name" content="CryptoStackHub">
<meta property="og:image" content="{image}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(desc)}">
<meta name="twitter:image" content="{image}">
{schema}
'''

def header(active=""):
    def cls(key): return ' class="active"' if active == key else ""
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{{{{TITLE}}}}</title>
<meta name="description" content="{{{{DESC}}}}">
<link rel="icon" type="image/png" href="/assets/images/favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/css/style.css?v=hero-visibility">
</head>
<body>
<div class="grain"></div>
<div class="progress"></div>
<header class="site-header">
  <div class="wrap header-inner">
    <a class="logo" href="/"><span class="logo-mark">{LOGO_SVG}</span><span>Crypto<b>StackHub</b></span></a>
    <button class="burger" aria-label="Open navigation menu" aria-expanded="false" aria-controls="site-navigation"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M4 7h16M4 12h16M4 17h16"/></svg></button>
    <nav class="main-nav" id="site-navigation">
      <a href="/defi/"{cls("defi")}>DeFi</a>
      <a href="/developers/"{cls("dev")}>Developers</a>
      <a href="/tax-compliance/"{cls("tax")}>Tax &amp; Compliance</a>
      <a href="/gaming-nfts/"{cls("gaming")}>Gaming &amp; NFTs</a>
      <a href="/resources/"{cls("resources")}>Resources</a>
      <a href="/glossary/"{cls("glossary")}>Glossary</a>
      <a href="/search/" class="nav-cta">Search</a>
    </nav>
  </div>
</header>
'''

def footer():
    return """
<footer class="site-footer">
  <div class="wrap">
    <div class="footer-grid">
      <div class="footer-brand">
        <a class="logo" href="/"><span class="logo-mark">""" + LOGO_SVG + """</span><span>Crypto<b>StackHub</b></span></a>
        <p>Independent, in-depth education on DeFi, blockchain engineering, crypto tax and Web3 gaming. No hype, no shilling — just signal.</p>
      </div>
      <div class="footer-col">
        <h4>Topics</h4>
        <a href="/defi/">DeFi &amp; Crypto Education</a>
        <a href="/developers/">Blockchain Development</a>
        <a href="/tax-compliance/">Crypto Tax &amp; Compliance</a>
        <a href="/gaming-nfts/">Web3 Gaming &amp; NFTs</a>
      </div>
      <div class="footer-col">
        <h4>Company</h4>
        <a href="/about/">About</a>
        <a href="/contact/">Contact</a>
        <a href="/write-for-us/">Write for Us</a>
        <a href="/advertise/">Advertise</a>
      </div>
      <div class="footer-col">
        <h4>Resources</h4>
        <a href="/resources/">Tools &amp; Resources</a>
        <a href="/glossary/">Glossary</a>
        <a href="/search/">Search</a>
      </div>
      <div class="footer-col">
        <h4>Legal</h4>
        <a href="/privacy-policy/">Privacy Policy</a>
        <a href="/terms/">Terms of Use</a>
        <a href="/disclaimer/">Disclaimer</a>
      </div>
    </div>
    <div class="footer-bottom">
      <span>© 2026 CryptoStackHub. Educational content only — not financial, legal or tax advice.</span>
      <span class="legal-links"><a href="/privacy-policy/">Privacy</a><a href="/terms/">Terms</a><a href="/disclaimer/">Disclaimer</a></span>
    </div>
  </div>
</footer>
<script src="/assets/js/main.js"></script>
</body>
</html>"""

def chips(cat):
    c = CATS[cat]
    return f'<span class="chip {c["cls"]}">{c["label"]}</span>'

def post_card(a, featured=False):
    c = CATS[a["cat"]]
    style = f'--tint2:{c["tint2"]};--tint3:{c["tint3"]}'
    return f"""<a class="post-card reveal" href="/articles/{a['slug']}/">
  <div class="post-visual"><div class="pv-bg" style="{style}"></div><div class="pv-icon">{ICONS[a['cat']]}</div></div>
  <div class="post-body">
    {chips(a['cat'])}
    <h3>{esc(a['title'])}</h3>
    <p>{esc(a['desc'])}</p>
    <div class="post-meta"><span>{a['read']} read</span><span>·</span><span>{a['date']}</span></div>
  </div>
</a>"""

def feature_card(a):
    c = CATS[a["cat"]]
    return f"""<a class="feature reveal" href="/articles/{a['slug']}/">
  <div class="post-visual"><div class="pv-bg" style="--tint2:{c['tint2']};--tint3:{c['tint3']}"></div><div class="pv-icon">{ICONS[a['cat']]}</div></div>
  <div class="post-body">
    {chips(a['cat'])}
    <h3>{esc(a['title'])}</h3>
    <p>{esc(a['desc'])}</p>
    <div class="post-meta"><span>{a['read']} read</span><span>·</span><span>Featured guide</span></div>
  </div>
</a>"""

def newsletter():
    return """<section><div class="wrap"><div class="newsletter reveal">
  <span class="eyebrow">Weekly Signal</span>
  <h2>One email. <span class="grad-text">Zero noise.</span></h2>
  <p>The week's most important developments across DeFi, blockchain engineering, crypto tax and Web3 gaming — distilled by humans who actually read the source material.</p>
  <form class="news-form"><input type="email" placeholder="you@example.com" required><button class="btn btn-primary" type="submit">Subscribe</button></form>
  <p class="news-note">Free forever. Unsubscribe anytime. We never share your email.</p>
</div></div></section>"""

def cat_cards():
    out = []
    blurbs = {
        "defi":  "Wallets, staking, liquidity pools and staying safe — DeFi explained from first principles.",
        "dev":   "Solidity, security, gas optimization and the tooling professionals use to ship on-chain.",
        "tax":   "Capital gains, DeFi income, NFTs and compliance — plain-language guidance that survives audits.",
        "gaming":"Player-owned economies, NFT utility and spotting rug pulls before they pull you.",
    }
    for k, c in CATS.items():
        n = sum(1 for a in ARTICLES if a["cat"] == k)
        out.append(f"""<a class="cat-card {c['cls']} reveal" href="/{c['slug']}/">
  <div class="cat-icon">{ICONS[k]}</div>
  <h3>{c['label']}</h3>
  <p>{blurbs[k]}</p>
  <span class="cat-meta">{n} in-depth guides →</span>
</a>""")
    return '<div class="cat-grid">' + "\n".join(out) + "</div>"

def crumbs(items):
    parts = ['<a href="/">Home</a>']
    for label, url in items[:-1]:
        parts.append(f'<span class="sep">/</span><a href="{url}">{label}</a>')
    parts.append(f'<span class="sep">/</span><span class="here">{items[-1][0]}</span>')
    return '<nav class="crumbs">' + "".join(parts) + "</nav>"

def write(path, html):
    full = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    breadcrumb_nav = re.search(r'<nav class="crumbs">(.*?)</nav>', html, re.S)
    breadcrumbs = [("Home", "/")]
    if breadcrumb_nav:
        matches = re.findall(r'<a href="([^"]*)">([^<]+)</a>|<span class="here">([^<]+)</span>', breadcrumb_nav.group(1))
        breadcrumbs = [(linked_label or current_label, url or "/" + path.replace("index.html","")) for url, linked_label, current_label in matches]
    title = re.search(r'<title>(.*?)</title>', html, re.S).group(1)
    desc = re.search(r'<meta name="description" content="([^"]*)">', html, re.S).group(1)
    article = None
    m = re.match(r'articles/([^/]+)/index\.html$', path)
    if m:
        article = next((a for a in ARTICLES if a["slug"] == m.group(1)), None)
    profile = None
    m = re.match(r'authors/([^/]+)/index\.html$', path)
    if m:
        profile = next((key for key, value in AUTHORS.items() if value["slug"] == m.group(1)), None)
    seo = seo_head("/" + path.replace("index.html",""), title, desc, breadcrumbs, article, profile)
    html = html.replace("</head>", seo + "</head>", 1)
    with open(full, "w", encoding="utf-8") as f:
        f.write(html)

def page(title, desc, body):
    return header().replace("{{TITLE}}", title).replace("{{DESC}}", esc(desc)) + body + footer()

# ---------------------------------------------------------------- article renderer
def render_article(a, idx):
    c = CATS[a["cat"]]
    toc = "".join(f'<a href="#s{i}">{esc(s["title"])}</a>' for i, s in enumerate(a["sections"]))
    secs_html = []
    for i, s in enumerate(a["sections"]):
        blocks = []
        for b in s["blocks"]:
            if b == "code":
                blocks.append(CODE_SNIPPET)
            elif b.startswith("list:"):
                items = "".join(f"<li>{esc(x)}</li>" for x in b[5:].split("|"))
                blocks.append(f"<ul>{items}</ul>")
            else:
                blocks.append(f"<p>{esc(b)}</p>")
        secs_html.append(f'<h2 id="s{i}">{esc(s["title"])}</h2>' + "\n".join(blocks))
    body = "\n".join(secs_html)
    if a["slug"] == "what-is-defi":
        body = f'''<figure class="article-figure"><img src="https://hebbkx1anhila5yf.public.blob.vercel-storage.com/IMAGE1-YZ0juMeTaU0SKgH2ReCpoWiDNaZzMo.png" alt="Ethereum and traditional finance connected by a question mark, illustrating the shift from legacy finance to DeFi"><figcaption>DeFi connects programmable blockchain networks with familiar financial services.</figcaption></figure>{body}<figure class="article-figure"><img src="https://hebbkx1anhila5yf.public.blob.vercel-storage.com/IMAGE2-RKeka3RO908nO14SgPd2vTOTl5KWSq.png" alt="Centralized exchange versus decentralized exchange comparison showing custody, KYC, security and fee differences"></figure><figure class="article-figure"><img src="https://hebbkx1anhila5yf.public.blob.vercel-storage.com/IMAGE3-vvpu5IffN2kXgPsWifHLo2Mh1zD0JB.png" alt="Global DeFi network with an Ethereum symbol connected to wallets, users, payments and lending"></figure><figure class="article-figure"><img src="https://hebbkx1anhila5yf.public.blob.vercel-storage.com/IMAGE4-0INFCrVTIsLsupgoprfsUE0D9B3xuN.png" alt="Ethereum connected to a bank and legal scales, representing open finance and regulation questions"></figure>'''

    # related: same category first, then others
    rel = [x for x in ARTICLES if x["cat"] == a["cat"] and x["slug"] != a["slug"]][:3]
    if len(rel) < 3:
        rel += [x for x in ARTICLES if x["cat"] != a["cat"]][:3 - len(rel)]

    cat_list = [x for x in ARTICLES if x["cat"] == a["cat"]]
    pos = [x["slug"] for x in cat_list].index(a["slug"])
    prev_a = cat_list[(pos - 1) % len(cat_list)]
    next_a = cat_list[(pos + 1) % len(cat_list)]

    faq = [{"@type":"Question","name":"What does DeFi mean?","acceptedAnswer":{"@type":"Answer","text":"DeFi means decentralized finance: financial applications built on public blockchains and governed by smart contracts rather than traditional intermediaries."}},{"@type":"Question","name":"What can you do with DeFi?","acceptedAnswer":{"@type":"Answer","text":"People use DeFi for token swaps, lending, borrowing, stablecoin payments, staking and other programmable financial strategies."}},{"@type":"Question","name":"Is DeFi safe?","acceptedAnswer":{"@type":"Answer","text":"DeFi carries smart-contract, market, oracle, governance and custody risks. Use established protocols, verify addresses and never risk more than you can afford to lose."}}]
    faq_schema = '<script type="application/ld+json">' + json.dumps({"@context":"https://schema.org","@type":"FAQPage","mainEntity":faq}, ensure_ascii=False, separators=(",", ":")) + '</script>' if a["slug"] == "what-is-defi" else ""
    faq_html = '<section class="faq"><h2 id="faq">Frequently asked questions</h2>' + "".join(f'<details><summary>{esc(item["name"])}</summary><p>{esc(item["acceptedAnswer"]["text"])}</p></details>' for item in faq) + '</section>' if a["slug"] == "what-is-defi" else ""
    html = f"""
<section class="page-hero" style="padding-bottom:0">
  <div class="hero-grid"></div>
  <div class="wrap-narrow article-head">
    {crumbs([(c["label"], f"/{c['slug']}/"), (a["title"], "")])}
    {chips(a['cat'])}
    <h1>{esc(a['title'])}</h1>
    <div class="article-meta"><span>By <a href="{author_url(a['author_key'])}">{esc(AUTHORS[a['author_key']]['name'])}</a></span><span>·</span><span>{a['date']}</span><span>·</span><span>{a['read']} read</span></div>
  </div>
</section>
<div class="wrap" style="margin-top:10px">
  <div class="article-layout">
    <article class="prose">
      <p class="lede">{esc(a['desc'])}</p>
      {body}
      {faq_html}
      {faq_schema}
      <div class="takeaways">
        <h3><svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6 9 17l-5-5"/></svg>Key takeaways</h3>
        <ul>{"".join(f"<li>{esc(t)}</li>" for t in a['takeaways'])}</ul>
      </div>
      <div class="disclaimer-box"><b>Educational content only.</b> This article is for informational purposes and is not financial, legal, tax or investment advice. Do your own research and consult qualified professionals before making decisions.</div>
      <div class="prev-next">
        <a class="pn-card" href="/articles/{prev_a['slug']}/"><span>← Previous in {c['short']}</span><b>{esc(prev_a['title'])}</b></a>
        <a class="pn-card next" href="/articles/{next_a['slug']}/"><span>Next in {c['short']} →</span><b>{esc(next_a['title'])}</b></a>
      </div>
    </article>
    <aside class="toc">
      <div class="toc-box"><h4>On this page</h4>{toc}</div>
      <div class="toc-share"><h4>Share</h4>
        <div class="share-row">
          <button data-share="copy" title="Copy link">&#128279;</button>
          <button data-share="x" title="Share on X"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M18.9 2H22l-6.8 7.8L23.3 22h-6.3l-4.9-6.4L6.4 22H3.3l7.3-8.3L1 2h6.5l4.4 5.9L18.9 2zm-1.1 18h1.7L7.6 3.8H5.8L17.8 20z"/></svg></button>
          <button data-share="native" title="Share"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><path d="m8.6 13.5 6.8 4M15.4 6.5l-6.8 4"/></svg></button>
        </div>
      </div>
    </aside>
  </div>
</div>
<section><div class="wrap">
  <div class="section-head"><h2>Keep reading</h2><a class="section-link" href="/{c['slug']}/">All {c['short']} guides →</a></div>
  <div class="card-grid">{"".join(post_card(x) for x in rel)}</div>
</div></section>
{newsletter()}
"""
    write(f"articles/{a['slug']}/index.html", page(f"{a['title']} — CryptoStackHub", a["desc"], html))

# ---------------------------------------------------------------- hub renderer
def render_hub(key):
    c = CATS[key]
    arts = [a for a in ARTICLES if a["cat"] == key]
    topics = sorted({w for a in arts for w in a["keywords"].split()[:6]})[:12]
    html = f"""
<section class="page-hero hub-hero hub-{c['slug'].replace("tax-compliance","tax").replace("gaming-nfts","gaming").replace("developers","developers")}">
  <div class="hero-grid"></div>
  <div class="orb-1 hero-orb" style="background:{c['tint2'].replace('.38','.16')}"></div>
  <div class="wrap">
    {crumbs([(c["label"], "")])}
    <span class="eyebrow">{c['tagline']}</span>
    <h1>{c['label'].split(" &")[0]} <span class="grad-text">{c['label'].split(" &")[1] if " &" in c['label'] else ""}</span></h1>
    <p class="lead">{c['desc']}</p>
    <div class="hub-topics">{"".join(f"<span>{esc(t)}</span>" for t in topics)}</div>
  </div>
</section>
<section style="padding-top:20px"><div class="wrap">
  {feature_card(arts[0])}
  <div class="section-head" style="margin-top:56px"><h2>All {c['short']} guides</h2><span class="section-link" style="color:var(--muted)">{len(arts)} articles</span></div>
  <div class="card-grid">{"".join(post_card(a) for a in arts[1:])}</div>
</div></section>
{newsletter()}
"""
    write(f"{c['slug']}/index.html", page(f"{c['label']} — CryptoStackHub", c["desc"], html))

# ---------------------------------------------------------------- static pages
def page_hero(crumb, eyebrow, title_html, lead):
    return f"""<section class="page-hero"><div class="hero-grid"></div><div class="wrap-narrow">
  {crumbs([(crumb, "")])}
  <span class="eyebrow">{eyebrow}</span>
  <h1>{title_html}</h1><p class="lead">{lead}</p>
</div></section>"""

def render_home():
    featured = ARTICLES[0]
    latest = ARTICLES[1:7]
    html = f"""
<section class="hero">
  <div class="hero-grid"></div>
  <div class="orb-1 hero-orb"></div><div class="orb-2 hero-orb"></div><div class="orb-3 hero-orb"></div>
  <div class="wrap">
    <span class="eyebrow">Independent Web3 Publication</span>
    <h1>Master the <span class="grad-text">on-chain world</span> — without the noise.</h1>
    <p class="lead">In-depth guides on DeFi, blockchain development, crypto tax &amp; compliance, and Web3 gaming. Written for people who want to understand how it actually works.</p>
    <div class="hero-actions">
      <a class="btn btn-primary" href="/defi/">Start Learning <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg></a>
      <a class="btn btn-ghost" href="/search/">Search 40+ Guides</a>
    </div>
    <div class="stats-strip reveal">
      <div class="stat"><b>40+</b><span>In-depth guides</span></div>
      <div class="stat"><b>4</b><span>Expert tracks</span></div>
      <div class="stat"><b>100%</b><span>Independent research</span></div>
      <div class="stat"><b>0</b><span>Sponsored shilling</span></div>
    </div>
  </div>
</section>
<section><div class="wrap">
  <div class="section-head"><div><h2>Choose your track</h2><p class="sub">Four deep libraries, one standard: clarity over hype.</p></div></div>
  {cat_cards()}
</div></section>
<section style="padding-top:0"><div class="wrap">
  <div class="section-head"><div><h2>Featured guide</h2></div></div>
  {feature_card(featured)}
</div></section>
<section style="padding-top:0"><div class="wrap">
  <div class="section-head"><div><h2>Latest from the library</h2><p class="sub">Fresh research across all four tracks.</p></div><a class="section-link" href="/search/">Browse everything →</a></div>
  <div class="card-grid">{"".join(post_card(a) for a in latest)}</div>
</div></section>
{newsletter()}
"""
    write("index.html", page("CryptoStackHub — DeFi, Blockchain Dev, Crypto Tax & Web3 Gaming", "In-depth guides on DeFi, blockchain development, crypto tax & compliance, and Web3 gaming. Clarity over hype.", html))

def render_search():
    html = page_hero("Search", "Find anything", "Search the <span class='grad-text'>library</span>", "Instant search across all 40+ guides on DeFi, development, tax and Web3 gaming.") + """
<section style="padding-top:0"><div class="wrap-narrow">
  <div class="search-wrap search-hero">
    <svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round"><circle cx="11" cy="11" r="7"/><path d="m21 21-4-4"/></svg>
    <input id="search-input" type="search" placeholder="Try “staking”, “solidity”, “capital gains”, “NFT”…" autocomplete="off">
  </div>
  <p class="search-count" id="search-count"></p>
  <div id="search-results"></div>
</div></section>
"""
    write("search/index.html", page("Search — CryptoStackHub", "Search all CryptoStackHub guides instantly.", html))

def render_about():
    html = page_hero("About", "Our story", "Signal in a sea of <span class='grad-text'>noise</span>", "CryptoStackHub exists because most crypto content is either hype, fear, or marketing in disguise. We write the guides we wished existed when we started.") + f"""
<section style="padding-top:0"><div class="wrap">
  <div class="split">
    <div>
      <h2>What we believe</h2>
      <p>Crypto is a genuinely important technology wrapped in an exhausting amount of grift. Understanding it shouldn't require reading whitepapers at 2am or learning which influencer to trust.</p>
      <p>Every CryptoStackHub guide is built the same way: start from first principles, explain the mechanism honestly, name the risks in plain language, and never — ever — tell you what to buy.</p>
      <ul class="tick-list">
        <li><svg viewBox="0 0 24 24" fill="none" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6 9 17l-5-5"/></svg>No sponsored content disguised as editorial</li>
        <li><svg viewBox="0 0 24 24" fill="none" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6 9 17l-5-5"/></svg>No token shilling, affiliate links are always disclosed</li>
        <li><svg viewBox="0 0 24 24" fill="none" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6 9 17l-5-5"/></svg>Every claim checked against primary sources</li>
      </ul>
    </div>
    <div class="value-grid" style="grid-template-columns:1fr">
      <div class="value-card"><div class="cat-icon cat-defi">{ICONS['defi']}</div><h3>Education first</h3><p>We optimize for your understanding, not our page views. If a topic needs 3,000 words, it gets 3,000 words.</p></div>
      <div class="value-card"><div class="cat-icon cat-tax">{ICONS['tax']}</div><h3>Honest about risk</h3><p>Every guide names what can go wrong. If that scares you away from something, the guide did its job.</p></div>
      <div class="value-card"><div class="cat-icon cat-dev">{ICONS['dev']}</div><h3>Built by practitioners</h3><p>Our contributors write contracts, run nodes, file the taxes and play the games they cover.</p></div>
    </div>
  </div>
</div></section>
{newsletter()}
"""
    write("about/index.html", page("About — CryptoStackHub", "CryptoStackHub is an independent Web3 education publication. No hype, no shilling — just signal.", html))

def contact_form(kind):
    fields = """
      <div class="form-field"><label>Your name</label><input type="text" required placeholder="Satoshi Nakamoto"></div>
      <div class="form-field"><label>Email</label><input type="email" required placeholder="you@example.com"></div>"""
    if kind == "write":
        fields += """
      <div class="form-field full"><label>Proposed topic</label><input type="text" required placeholder="e.g. Account abstraction for game developers"></div>
      <div class="form-field full"><label>Pitch & writing samples</label><textarea required placeholder="Summarize your article idea in 3–5 sentences and link 1–2 published samples."></textarea></div>"""
    elif kind == "advertise":
        fields += """
      <div class="form-field"><label>Company</label><input type="text" required placeholder="Acme Protocol"></div>
      <div class="form-field"><label>Budget range</label><select><option>Under $2k / month</option><option>$2k – $10k / month</option><option>$10k+ / month</option></select></div>
      <div class="form-field full"><label>What are you promoting?</label><textarea required placeholder="Tell us about your product and campaign goals."></textarea></div>"""
    else:
        fields += """
      <div class="form-field full"><label>Subject</label><input type="text" required placeholder="How can we help?"></div>
      <div class="form-field full"><label>Message</label><textarea required placeholder="Your message…"></textarea></div>"""
    return f"""<div class="form-card reveal"><form class="form-grid" data-demo-form>{fields}
  <div class="form-field full"><button class="btn btn-primary" type="submit">Send message</button></div>
</form></div>"""

def render_contact():
    html = page_hero("Contact", "Get in touch", "Talk to a <span class='grad-text'>human</span>", "Questions, corrections, partnership ideas — we read everything and reply within two business days.") + f"""
<section style="padding-top:0"><div class="wrap-narrow">{contact_form('contact')}</div></section>
"""
    write("contact/index.html", page("Contact — CryptoStackHub", "Contact the CryptoStackHub team.", html))

def render_write():
    html = page_hero("Write for Us", "Contribute", "Write for <span class='grad-text'>CryptoStackHub</span>", "We publish deep, honest guides from practitioners. If you build, trade, audit or analyze — and can write clearly — we want your pitch.") + """
<section style="padding-top:0"><div class="wrap">
  <div class="split">
    <div>
      <h2>What we're looking for</h2>
      <p>Original, in-depth pieces (1,500+ words) in our four tracks. We favor mechanism over news, and honesty over excitement. Every piece must name its risks and trade-offs.</p>
      <ul class="tick-list">
        <li><svg viewBox="0 0 24 24" fill="none" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6 9 17l-5-5"/></svg>Technical tutorials with real, tested code</li>
        <li><svg viewBox="0 0 24 24" fill="none" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6 9 17l-5-5"/></svg>First-principles explainers with original diagrams</li>
        <li><svg viewBox="0 0 24 24" fill="none" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6 9 17l-5-5"/></svg>Tax &amp; compliance analysis from qualified professionals</li>
        <li><svg viewBox="0 0 24 24" fill="none" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6 9 17l-5-5"/></svg>Post-mortems and case studies from real projects</li>
      </ul>
      <p style="margin-top:18px;color:var(--muted);font-size:.9rem">We pay competitive rates for accepted pieces. We do not accept AI-generated submissions, promotional content, or anything you wouldn't sign your real name to.</p>
    </div>
    <div>""" + contact_form("write") + """</div>
  </div>
</div></section>
"""
    write("write-for-us/index.html", page("Write for Us — CryptoStackHub", "Contribute in-depth Web3 guides to CryptoStackHub.", html))

def render_advertise():
    html = page_hero("Advertise", "Partnerships", "Reach readers who <span class='grad-text'>actually build</span>", "Our audience is developers, DeFi power users and finance professionals — people who read 3,000-word guides for fun. If your product serves them, let's talk.") + """
<section style="padding-top:0"><div class="wrap">
  <div class="stat-cards reveal">
    <div class="stat-card"><b>120k+</b><span>Monthly readers</span></div>
    <div class="stat-card"><b>6:40</b><span>Avg. time on page</span></div>
    <div class="stat-card"><b>68%</b><span>Developers &amp; finance pros</span></div>
  </div>
  <div class="split" style="margin-top:20px">
    <div>
      <h2>Formats & principles</h2>
      <ul class="tick-list">
        <li><svg viewBox="0 0 24 24" fill="none" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6 9 17l-5-5"/></svg>Newsletter sponsorships — clearly labeled, one per issue</li>
        <li><svg viewBox="0 0 24 24" fill="none" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6 9 17l-5-5"/></svg>Category sponsorships — tasteful placement on hub pages</li>
        <li><svg viewBox="0 0 24 24" fill="none" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6 9 17l-5-5"/></svg>Never: disguised editorial, token promotion, or anything we wouldn't defend publicly</li>
      </ul>
      <p style="margin-top:16px">Every sponsorship is disclosed. Editorial independence is not negotiable — it's the entire product.</p>
    </div>
    <div>""" + contact_form("advertise") + """</div>
  </div>
</div></section>
"""
    write("advertise/index.html", page("Advertise — CryptoStackHub", "Advertise to CryptoStackHub's audience of Web3 builders and power users.", html))

LEGAL_INTRO = '<p class="updated">Last updated: September 2026</p>'

def render_legal(slug, title, eyebrow, lead, sections):
    secs = "".join(f"<h2>{t}</h2><p>{b}</p>" for t, b in sections)
    html = page_hero(title, eyebrow, f"{title.split(' ')[0]} <span class='grad-text'>{' '.join(title.split(' ')[1:])}</span>", lead) + f"""
<section style="padding-top:0"><div class="wrap-narrow legal">{LEGAL_INTRO}{secs}</div></section>
"""
    write(f"{slug}/index.html", page(f"{title} — CryptoStackHub", lead, html))

def render_privacy():
    render_legal("privacy-policy", "Privacy Policy", "Legal", "How we collect, use and protect your data — in language you can actually read.", [
        ("1. What we collect", "We collect the minimum: your email address if you subscribe to the newsletter, standard analytics (pages visited, approximate region, device type), and anything you voluntarily send us via forms. We do not use invasive tracking pixels or sell data to brokers."),
        ("2. How we use it", "Your email is used only to send the newsletter you asked for. Analytics are used in aggregate to understand which guides help readers. Contact form submissions are used solely to respond to you."),
        ("3. Cookies", "We use a small number of functional cookies and privacy-respecting analytics. You can block cookies in your browser; the site will still work."),
        ("4. Third parties", "If you click external links, those sites have their own policies. Newsletter delivery is handled by an email provider bound by a data-processing agreement. We never sell or rent your personal information."),
        ("5. Your rights", "You may request access, correction or deletion of your personal data at any time via the contact page. Newsletter emails include a one-click unsubscribe link."),
        ("6. Changes", "If this policy changes materially, we will note it on this page with a new 'last updated' date."),
    ])

def render_terms():
    render_legal("terms", "Terms of Use", "Legal", "The rules of the road for using CryptoStackHub.", [
        ("1. Acceptance", "By using this website you agree to these terms. If you don't agree, please don't use the site."),
        ("2. Educational content", "All content is provided for general education and information only. It is not financial, investment, legal, accounting or tax advice, and it does not consider your personal circumstances."),
        ("3. Accuracy", "We work hard to be accurate, but the crypto landscape changes fast. Content may become outdated. You are responsible for verifying information before acting on it."),
        ("4. Intellectual property", "Original articles, design and code samples on this site are our property. You may share links and brief quotes with attribution; you may not republish full articles without permission."),
        ("5. No liability", "To the maximum extent permitted by law, we are not liable for any losses arising from use of this site or reliance on its content, including losses from protocols, wallets, or tax positions discussed."),
        ("6. External links", "We link to third-party tools and services for convenience. We don't control and aren't responsible for their content or practices."),
    ])

def render_disclaimer():
    render_legal("disclaimer", "Disclaimer", "Legal", "Please read this before acting on anything you read here.", [
        ("Not financial advice", "Nothing on CryptoStackHub constitutes financial, investment, legal or tax advice. We are educators and writers, not your advisor. Cryptocurrency investments are high-risk; you can lose everything you put in."),
        ("Do your own research", "Every protocol, token, wallet and strategy discussed carries risk, including total loss. Smart contracts can be exploited, stablecoins can de-peg, and regulations can change overnight. Verify everything against primary sources."),
        ("Tax content", "Tax treatment of crypto varies by jurisdiction and changes frequently. Our tax guides are general education, not advice for your situation. Consult a qualified tax professional in your jurisdiction before filing."),
        ("Affiliates & sponsors", "Where we use affiliate links or accept sponsorships, they are disclosed on the page. Editorial opinions are never for sale."),
        ("No guarantees", "Content is provided 'as is' without warranty of any kind. Use of this site is at your own risk."),
    ])

def render_resources():
    groups = [
        ("defi", "DeFi Essentials", "Tools every DeFi user should bookmark before their first swap.", [
            ("Block explorers", "Verify contracts, transactions and addresses before you trust them."),
            ("Portfolio trackers", "See positions across wallets and chains in one dashboard."),
            ("Approval revokers", "Audit and revoke stale token allowances monthly."),
            ("DeFi analytics", "TVL, yields and protocol revenue from primary on-chain data."),
        ]),
        ("dev", "Developer Stack", "The toolchain professional smart contract engineers rely on.", [
            ("Foundry / Hardhat", "Compile, test, fuzz and deploy — the two industry-standard frameworks."),
            ("Remix IDE", "Zero-setup browser IDE for learning and quick experiments."),
            ("OpenZeppelin", "Audited contract libraries and security tooling. Don't roll your own."),
            ("Slither & fuzzers", "Static analysis and property-based testing before every audit."),
        ]),
        ("tax", "Tax & Compliance", "Stay organized long before filing season.", [
            ("Crypto tax software", "Aggregate wallets and exchanges; reconcile flagged transactions manually."),
            ("Cost basis trackers", "FIFO/LIFO/HIFO tracking across every venue you use."),
            ("CARF/DAC8 resources", "Understand what platforms now report about you automatically."),
            ("Professional directories", "Find accountants who actually understand DeFi and NFTs."),
        ]),
        ("gaming", "Gaming & NFTs", "Navigate player-owned economies safely.", [
            ("Gaming wallets", "Session-key smart wallets and hardware options for valuable assets."),
            ("Marketplace aggregators", "Real liquidity data beyond a single marketplace's floor price."),
            ("Contract checkers", "Verify mint contracts before signing anything."),
            ("Rug-pull databases", "Track records of teams and projects before you buy in."),
        ]),
    ]
    body = page_hero("Resources", "Curated toolkit", "The <span class='grad-text'>toolkit</span> we actually use", "Hand-picked tools for each of our four tracks. No pay-to-list placements — ever.")
    body += '<section style="padding-top:0"><div class="wrap">'
    icon_r = '<svg viewBox="0 0 24 24" fill="none" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/></svg>'
    for key, name, desc, items in groups:
        c = CATS[key]
        rows = "".join(f"""<a class="resource-item {c['cls']} reveal" href="/{c['slug']}/">
  <div class="r-icon">{icon_r}</div><div><b>{t}</b><p>{d}</p></div></a>""" for t, d in items)
        body += f"""<div class="resource-group {c['cls']}">
  <h2><span class="dot"></span>{name}</h2><p>{desc}</p>
  <div class="resource-list">{rows}</div></div>"""
    body += "</div></section>" + newsletter()
    write("resources/index.html", page("Resources — CryptoStackHub", "Curated tools for DeFi, blockchain development, crypto tax and Web3 gaming.", body))

GLOSSARY = [
    ("Airdrop","A","Free distribution of tokens to wallets, usually for marketing or rewarding early users. Taxable as income on receipt in most jurisdictions."),
    ("AMM","A","Automated Market Maker — a DEX design where a formula (not an order book) prices trades against pooled liquidity."),
    ("APY","A","Annual Percentage Yield — the compounded annual return on a position. Compare APYs only alongside their risk sources."),
    ("Bridge","B","A protocol that moves assets between blockchains. Historically the most exploited category in crypto — treat with caution."),
    ("Cold Wallet","C","A wallet whose keys never touch an internet-connected device — typically a hardware wallet. The baseline for serious holdings."),
    ("Composability","C","The ability of DeFi protocols to plug into each other like Lego bricks, enabling complex transactions in one step."),
    ("Cost Basis","C","What you paid for an asset (including fees). The number your capital gain is measured against."),
    ("DAO","D","Decentralized Autonomous Organization — governance by token holders voting on-chain, with execution by smart contracts."),
    ("DEX","D","Decentralized Exchange — trades settle on-chain from your own wallet. You keep custody; you bear the smart contract risk."),
    ("EVM","E","Ethereum Virtual Machine — the runtime executing smart contracts on Ethereum and dozens of compatible chains."),
    ("Flash Loan","F","An uncollateralized loan that must be repaid within one transaction. Powers arbitrage — and many famous exploits."),
    ("Gas","G","The fee paid to execute computation on a blockchain. Priced per unit of work; spikes with network demand."),
    ("HODL","H","Hold On for Dear Life — the strategy of simply not selling. Tax-efficient in many jurisdictions; psychologically brutal."),
    ("Impermanent Loss","I","The opportunity cost LPs suffer when pooled token prices diverge, versus simply holding. Realized on withdrawal."),
    ("Layer 2","L","A network that processes transactions off Ethereum's main chain and posts proofs back to it, inheriting its security."),
    ("Liquidity Pool","L","A smart contract holding two (or more) tokens that traders swap against; providers earn fees and bear IL."),
    ("MEV","M","Maximal Extractable Value — profit block producers (and searchers) extract by ordering transactions, e.g. sandwich attacks."),
    ("NFT","N","Non-Fungible Token — a unique on-chain token representing ownership of an asset: art, items, credentials, access."),
    ("Oracle","O","A service feeding real-world data (prices, weather) into smart contracts. Manipulated oracles have drained many protocols."),
    ("Private Key","P","The secret that controls your funds. Whoever holds it owns the assets — there is no password reset."),
    ("Reentrancy","R","An attack where an external call re-enters a function before state updates. The DAO hack's weapon; guarded against with checks-effects-interactions."),
    ("Rug Pull","R","When developers drain liquidity or dump insider tokens and abandon the project. Due diligence is the only vaccine."),
    ("Seed Phrase","S","The 12–24 words that regenerate your entire wallet. Never type it into any website; never store it digitally."),
    ("Slashing","S","Destruction of part of a validator's staked collateral for misbehavior or downtime on proof-of-stake networks."),
    ("Smart Contract","S","Self-executing code on a blockchain that holds funds and enforces rules exactly as written — bugs included."),
    ("Stablecoin","S","A token pegged to an external reference (usually USD) via fiat reserves, crypto collateral, or algorithms."),
    ("Staking","S","Locking tokens to secure a proof-of-stake network in exchange for rewards from issuance and fees."),
    ("TVL","T","Total Value Locked — the assets deposited in a protocol. A rough health metric, easily gamed; read alongside revenue."),
    ("Validator","V","A node that proposes and attests to blocks on proof-of-stake networks, backed by staked collateral."),
    ("Yield Farming","Y","Actively supplying liquidity or capital across DeFi protocols to earn fees and incentive tokens. Higher yield, higher risk."),
]

def render_glossary():
    letters = sorted({t[1] for t in GLOSSARY})
    nav = "".join(f'<a href="#g-{l}">{l}</a>' for l in letters)
    terms = "".join(f"""<div class="term reveal" id="g-{l}"><h3>{esc(t)}<em>{l}</em></h3><p>{esc(d)}</p></div>""" for t, l, d in GLOSSARY)
    body = page_hero("Glossary", "Web3, decoded", "The <span class='grad-text'>glossary</span>", "Thirty terms that unlock ninety percent of Web3 conversations — defined without jargon.") + f"""
<section style="padding-top:0"><div class="wrap">
  <div class="glossary-nav">{nav}</div>
  <div class="glossary-grid">{terms}</div>
</div></section>
{newsletter()}
"""
    write("glossary/index.html", page("Glossary — CryptoStackHub", "Plain-language definitions of essential Web3, DeFi and crypto terms.", body))

# ---------------------------------------------------------------- author pages
def render_author(author_key):
    a = AUTHORS[author_key]
    authored = [x for x in ARTICLES if x["author_key"] == author_key]
    body = f"""<section class="page-hero"><div class="hero-grid"></div><div class="wrap-narrow">
  {crumbs([("Authors", "/authors/"), (a["name"], "")])}
  <span class="eyebrow">{esc(a["role"])}</span>
  <h1>{esc(a["name"])}</h1>
  <p class="lead">{esc(a["bio"])}</p>
</div></section>
<section style="padding-top:0"><div class="wrap">
  <div class="section-head"><div><h2>Articles by {esc(a["name"])}</h2><p class="sub">{len(authored)} published guides.</p></div></div>
  <div class="card-grid">{"".join(post_card(x) for x in authored)}</div>
</div></section>
{newsletter()}
"""
    write(f"authors/{a['slug']}/index.html", page(f"{a['name']} — CryptoStackHub", a["bio"], body))

def render_authors_index():
    cards = "".join(f"""<a class="cat-card reveal" href="{author_url(k)}"><h3>{esc(v["name"])}</h3><p><b>{esc(v["role"])}</b></p><p>{esc(v["bio"])}</p><span class="cat-meta">{sum(1 for x in ARTICLES if x["author_key"] == k)} articles →</span></a>""" for k, v in AUTHORS.items())
    body = page_hero("Authors", "Editorial team", "Meet the <span class='grad-text'>authors</span>", "The editorial desks behind CryptoStackHub's independent guides.") + f"""<section style="padding-top:0"><div class="wrap"><div class="cat-grid">{cards}</div></div></section>{newsletter()}"""
    write("authors/index.html", page("Authors — CryptoStackHub", "Meet the editorial authors behind CryptoStackHub.", body))

# ---------------------------------------------------------------- build
def main():
    for i, a in enumerate(ARTICLES):
        a["date"] = DATES[i]
        a["dateModified"] = a["date"]
    for i, a in enumerate(ARTICLES):
        render_article(a, i)
    render_authors_index()
    for key in AUTHORS:
        render_author(key)
    for key in CATS:
        render_hub(key)
    render_home()
    render_search()
    render_about()
    render_contact()
    render_write()
    render_advertise()
    render_privacy()
    render_terms()
    render_disclaimer()
    render_resources()
    render_glossary()

    # search index
    idx = [dict(title=a["title"], description=a["desc"], url=f"/articles/{a['slug']}/",
                category=CATS[a["cat"]]["label"], catClass=CATS[a["cat"]]["cls"], keywords=a["keywords"])
           for a in ARTICLES]
    with open(os.path.join(OUT, "assets/search-index.json"), "w") as f:
        json.dump(idx, f, indent=1)

    # sitemap + robots
    static_urls = [
        ("/", "2026-09-08"), ("/search/", "2026-09-08"), ("/about/", "2026-09-08"),
        ("/contact/", "2026-09-08"), ("/write-for-us/", "2026-09-08"), ("/advertise/", "2026-09-08"),
        ("/privacy-policy/", "2026-09-08"), ("/terms/", "2026-09-08"), ("/disclaimer/", "2026-09-08"),
        ("/resources/", "2026-09-08"), ("/glossary/", "2026-09-08"), ("/authors/", "2026-09-08")
    ]
    static_urls += [(f"/{c['slug']}/", "2026-09-08") for c in CATS.values()]
    static_urls += [(author_url(k), "2026-09-08") for k in AUTHORS]
    article_urls = [(f"/articles/{a['slug']}/", a["dateModified"]) for a in ARTICLES]
    urls = static_urls + article_urls
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    sm += "\n".join(f"  <url><loc>https://cryptostackhub.com{u}</loc><lastmod>{lastmod}</lastmod></url>" for u, lastmod in urls)
    sm += "\n</urlset>\n"
    with open(os.path.join(OUT, "sitemap.xml"), "w") as f:
        f.write(sm)
    with open(os.path.join(OUT, "robots.txt"), "w") as f:
        f.write("User-agent: *\nAllow: /\nSitemap: https://cryptostackhub.com/sitemap.xml\n")

    count = sum(len(files) for _, _, files in os.walk(OUT) if "build" not in files)
    print(f"Built OK — {len(ARTICLES)} articles, {len(urls)} pages total.")

if __name__ == "__main__":
    main()
