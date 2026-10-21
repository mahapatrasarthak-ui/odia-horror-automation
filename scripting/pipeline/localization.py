"""Centralized language and culture settings for the story generator.

The profile is deliberately small and readable. Creative prompts can grow, but the
language choice should have one source of truth so a single Hindi fallback cannot
silently override an Odia run.
"""
from __future__ import annotations

import os
from typing import Final

DEFAULT_LANGUAGE = os.environ.get("YOUTUBE_LANGUAGE", "Odia")

_LOCALES: Final[dict[str, dict[str, str]]] = {
    "hindi": {
        "language_name": "Hindi",
        "language_code": "hi-IN",
        "script_name": "Devanagari",
        "region": "North India",
        "culture_mode": "Hindi-localized",
        # Kept for compatibility with existing pipeline.json files. A later
        # schema migration can rename this to dialogue_text everywhere.
        "dialogue_field": "devanagari_dialogue",
        "dialogue_label": "DEVANAGARI ONLY",
        "accent_instruction": "100% native North Indian Hindi accent; no Western or English cadence.",
        "default_concept": "बारिश में उत्तर भारतीय कस्बे की आख़िरी बस; एक अकेली महिला यात्री, तीसरी खाली सीट, और पिछली दुर्घटना में मरी आत्मा",
        "default_title": "आख़िरी बस की तीसरी सीट (Aakhri Bus Ki Teesri Seat)",
        "default_hook": "बरसाती रात की आख़िरी बस में तीसरी सीट हर पड़ाव पर भीग जाती है, जबकि उस पर कोई दिखाई नहीं देता।",
        "default_entity_archetype": "Pret-aatma",
        "default_monster": "बस की तीसरी सीट की प्रेत-आत्मा",
        "hook_prompt": "Write one single-sentence Devanagari Hindi folk-horror hook for this exact video title: {title}. Keep it original, set in a fictional North Indian town, and use no real people or places. Return only the hook.",
        "story_follow_up": "Write the full 130–155-word Hindi story now. Use only fictional named people and a fictional unnamed North Indian town. Every line that will be spoken must be written in Devanagari. One female protagonist, one driver, and one spectral woman. Do not switch to another premise.",
        "narrator_direction": "Adult Hindi folk-horror narrator. Calm, suspenseful, native North Indian Hindi pronunciation; no English or Western cadence. Read exactly the supplied text; add no dialogue or stage directions.",
        "character_voice_fallback": "Native North Indian Hindi pronunciation",
        "character_descriptor_fallback": "उत्तर भारतीय लहजा",
        "title_font": "Georgia",
        "title_kicker": "H I N D I   F O L K   H O R R O R",
        "fallback_title": "Hindi Folk Horror",
    },
    "odia": {
        "language_name": "Odia",
        "language_code": "or-IN",
        "script_name": "Odia",
        "region": "Odisha, India",
        "culture_mode": "Odisha-localized; episode setting remains configurable",
        # Kept for compatibility with the current production/editor contract.
        "dialogue_field": "devanagari_dialogue",
        "dialogue_label": "ODIA SCRIPT ONLY",
        "accent_instruction": "100% native Odia pronunciation and Odia speech rhythm; no Hindi, English, or Western cadence.",
        "default_concept": "ଓଡ଼ିଶାର ଏକ କଳ୍ପିତ ଛୋଟ ସହରରେ ବର୍ଷା ରାତିର ଶେଷ ବସ୍; ଏକାକୀ ଯୁବତୀ ଯାତ୍ରୀ, ତୃତୀୟ ଖାଲି ସିଟ୍, ଏବଂ ପୁରୁଣା ଦୁର୍ଘଟଣାରେ ମରିଥିବା ଆତ୍ମା",
        "default_title": "ଶେଷ ବସର ତୃତୀୟ ସିଟ୍ (Shesha Basara Trutiya Sit)",
        "default_hook": "ବର୍ଷାଭିଜା ରାତିର ଶେଷ ବସର ତୃତୀୟ ସିଟ୍‌ଟି ପ୍ରତ୍ୟେକ ଷ୍ଟପ୍‌ରେ ଭିଜିଯାଏ—ଯଦିଓ ସେଠାରେ କେହି ବସିନାହାନ୍ତି।",
        "default_entity_archetype": "ପ୍ରେତାତ୍ମା",
        "default_monster": "ବସର ତୃତୀୟ ସିଟ୍‌ର ପ୍ରେତାତ୍ମା",
        "hook_prompt": "Write one single-sentence natural Odia folk-horror hook in Odia script for this exact video title: {title}. Set it in an original fictional place in Odisha; do not use real people or unverified real-place claims. Return only the hook.",
        "story_follow_up": "Write the full 130–155-word story in natural spoken Odia. Use an original fictional named cast and a fictional place in Odisha. All spoken narration and dialogue must be written in Odia script. Keep one female protagonist, one driver, and one spectral woman only if they fit the locked premise. Do not switch premises.",
        "narrator_direction": "Adult Odia folk-horror narrator. Calm, suspenseful, natural Odia pronunciation and rhythm; no Hindi, English, or Western cadence. Read exactly the supplied text; add no dialogue or stage directions.",
        "character_voice_fallback": "Native Odia pronunciation",
        "character_descriptor_fallback": "Odia speech style",
        "title_font": "Noto Sans Oriya",
        "title_kicker": "O D I A   F O L K   H O R R O R",
        "fallback_title": "Odia Folk Horror",
    },
}

_ALIASES = {
    "hi": "hindi",
    "hi-in": "hindi",
    "hindi": "hindi",
    "or": "odia",
    "or-in": "odia",
    "odia": "odia",
}


def get_localization(language: str | None = None) -> dict[str, str]:
    """Return a copy of the selected locale profile.

    The default on this Odia fork is Odia. Set YOUTUBE_LANGUAGE=Hindi or pass
    --language Hindi to reproduce the original Hindi path.
    """
    requested = str(language or DEFAULT_LANGUAGE).strip().lower().replace("_", "-")
    key = _ALIASES.get(requested, requested)
    if key not in _LOCALES:
        supported = ", ".join(sorted(_LOCALES))
        raise ValueError(f"Unsupported language {language!r}; choose one of: {supported}")
    return dict(_LOCALES[key])

