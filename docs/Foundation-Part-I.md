# Temporal Liquidity Market (TLM)

# Foundation Statement — Part I: Foundations

**Version:** 1.0
**Release:** TLM Public Release 1 (PR1)
**Status:** Public Draft
**Last Updated:** July 2026

---

# 0. Abstract

Temporal Liquidity Market (TLM) is an open research framework for **temporal market design** in blockchain protocols.

Over the past several years, Ethereum has significantly advanced decentralized blockspace allocation through innovations such as EIP-1559, Proposer-Builder Separation (PBS), and Enshrined PBS (ePBS). These developments have substantially improved price discovery, decentralized block construction, protocol robustness, and market efficiency.

TLM begins with the observation that decentralized execution markets coordinate demand primarily through **price**, while another important economic characteristic of demand remains largely implicit: its flexibility with respect to execution time.

TLM introduces **Temporal Liquidity**, defined as the **economic flexibility of demand with respect to execution time**, as a new conceptual framework for understanding and coordinating execution markets.

Rather than proposing a single protocol mechanism, TLM establishes a research framework for representing, communicating, and coordinating Temporal Liquidity as a protocol-visible economic signal.

The objective is to build upon existing Ethereum protocol architecture while encouraging open research into the next generation of decentralized market design.

---

# 1. Introduction & Motivation

## 1.1 Background

Blockchain protocols have evolved from simple transaction processing systems into increasingly sophisticated decentralized marketplaces.

Ethereum, in particular, has pioneered protocol-level market design through innovations such as EIP-1559, Proposer-Builder Separation (PBS), and the ongoing development of Enshrined PBS (ePBS). These advances demonstrate that protocol design can substantially improve market efficiency while preserving decentralization and open participation.

The evolution of Ethereum fee markets illustrates an important principle: protocols need not merely execute markets—they can actively provide market infrastructure that enables participants to coordinate more effectively.

TLM is motivated by the belief that this evolution is not yet complete.

---

## 1.2 The Missing Economic Dimension

Current blockchain protocols primarily coordinate demand through economic signals based on **price**.

Users express how much they are willing to pay for execution, and protocol participants coordinate around those signals.

However, execution demand is inherently multi-dimensional.

Different transactions possess different economic requirements regarding execution time.

Some transactions require immediate execution because their economic value deteriorates rapidly.

Others remain economically valuable across much broader execution windows and may willingly exchange execution speed for lower transaction cost.

These differences are only partially represented by today's fee markets.

As a result, an important aspect of user demand remains implicit throughout the execution pipeline.

---

## 1.3 Temporal Liquidity

TLM proposes that the missing dimension is not simply "time," but **Temporal Liquidity**.

Temporal Liquidity characterizes the economic flexibility of demand with respect to execution time.

Just as traditional liquidity describes economic flexibility with respect to price, Temporal Liquidity describes economic flexibility with respect to when execution occurs.

Making Temporal Liquidity protocol-visible does not require the protocol to determine users' utility.

Instead, it provides market participants with richer information through which decentralized coordination may emerge.

This distinction between **making information visible** and **making decisions centrally** is one of the guiding principles of TLM.

---

## 1.4 A Framework Rather Than a Mechanism

TLM should not be viewed as a proposal for a single protocol mechanism.

Instead, it establishes a conceptual framework within which multiple protocol designs, market mechanisms, and implementation strategies may be explored.

Candidate mechanisms—including Temporal Liquidity Reserve (TLR), temporal preference representations, adaptive protocol parameters, and future protocol innovations—should be regarded as possible realizations of the broader framework rather than the framework itself.

This distinction allows TLM to remain mechanism-neutral while encouraging open experimentation and collaboration.

---

## 1.5 Research Philosophy

TLM adopts several principles that guide the remainder of this document.

First, protocol evolution should build upon existing Ethereum architecture rather than replace it.

Second, richer protocol-visible information should improve decentralized coordination without reducing participant autonomy.

Third, protocol mechanisms should preserve participant neutrality, transparency, and decentralized incentives.

Finally, the project views temporal market design as an open research direction rather than a completed theory.

The purpose of this Foundation Statement is therefore not to prescribe definitive solutions, but to establish a common conceptual language through which future research and protocol development can proceed.
