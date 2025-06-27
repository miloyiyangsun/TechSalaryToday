#!/usr/bin/env python3
"""
Test script for Groq translation functionality.
测试 Groq 翻译功能的脚本。
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from poc_scraper import groq_translator


def test_basic_translation():
    """Test basic Dutch to English translation."""
    print("🧪 Testing Basic Translation...")
    print("-" * 50)

    # Test cases
    test_texts = [
        "Hallo, hoe gaat het met je?",
        "Wij zoeken een ervaren software ontwikkelaar.",
        "Je werkt in een dynamisch team van professionals.",
        "Salaris tussen €50.000 en €70.000 per jaar.",
        "Functie-eisen: HBO/WO diploma, 3+ jaar ervaring",
    ]

    for i, dutch_text in enumerate(test_texts, 1):
        print(f"\n{i}. Testing translation:")
        print(f"   Dutch:   {dutch_text}")

        try:
            english_text = groq_translator.translate_text(dutch_text)
            print(f"   English: {english_text}")
            print(f"   ✅ Success")
        except Exception as e:
            print(f"   ❌ Error: {e}")

    print("\n" + "=" * 50)


def test_job_posting_translation():
    """Test translation of a realistic job posting."""
    print("🧪 Testing Job Posting Translation...")
    print("-" * 50)

    job_posting = """
    Software Developer - Amsterdam
    
    Wij zijn op zoek naar een ervaren software developer die ons team wil versterken. 
    Je gaat werken aan innovatieve projecten en hebt de kans om je vaardigheden verder te ontwikkelen.
    
    Functie-eisen:
    - HBO/WO diploma in Computer Science of vergelijkbaar
    - Minimaal 3 jaar ervaring met Python en JavaScript
    - Ervaring met React en Node.js is een pré
    - Goede communicatieve vaardigheden
    
    Wat bieden wij:
    - Salaris tussen €55.000 - €75.000 per jaar
    - 25 vakantiedagen
    - Flexibele werktijden
    - Thuiswerken mogelijk
    """

    print("Original Dutch job posting:")
    print(job_posting)
    print("\n" + "-" * 30 + " TRANSLATION " + "-" * 30)

    try:
        translated = groq_translator.translate_text(job_posting)
        print("Translated English job posting:")
        print(translated)
        print("\n✅ Translation successful!")
    except Exception as e:
        print(f"❌ Translation failed: {e}")

    print("\n" + "=" * 50)


def test_performance():
    """Test translation performance and speed."""
    print("🧪 Testing Translation Performance...")
    print("-" * 50)

    import time

    test_text = "Wij zoeken een ervaren software engineer voor ons team in Amsterdam."

    print(f"Testing translation speed with text: '{test_text}'")
    print("Performing 3 translations...")

    times = []
    for i in range(3):
        start_time = time.time()
        try:
            result = groq_translator.translate_text(test_text)
            end_time = time.time()
            duration = end_time - start_time
            times.append(duration)
            print(f"  Translation {i+1}: {duration:.2f}s - {result}")
        except Exception as e:
            print(f"  Translation {i+1}: FAILED - {e}")

    if times:
        avg_time = sum(times) / len(times)
        print(f"\n📊 Performance Summary:")
        print(f"   Average time: {avg_time:.2f}s")
        print(f"   Fastest: {min(times):.2f}s")
        print(f"   Slowest: {max(times):.2f}s")

    print("\n" + "=" * 50)


if __name__ == "__main__":
    print("🚀 Groq Translation Test Suite")
    print("=" * 50)

    try:
        test_basic_translation()
        test_job_posting_translation()
        test_performance()

        print("\n🎉 All tests completed!")
        print("Your Groq translation integration is ready to use!")

    except Exception as e:
        print(f"\n❌ Test suite failed: {e}")
        print("Please check your Groq API key and internet connection.")
