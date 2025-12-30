import subprocess
import json
import os

# ---------------- FILE BASED MEMORY ----------------
MEMORY_FILE = "memory.json"
NOTES_FILE = "notes.txt"

def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_memory(memory):
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(memory, f, ensure_ascii=False, indent=2)

# load memory at start
memory = load_memory()

# ---------------- AI FUNCTION ----------------
def ask_ai(prompt):
    result = subprocess.run(
        ["ollama", "run", "phi3", prompt],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
        errors="ignore"
    )
    return result.stdout.strip()

# ---------------- CALCULATOR TOOL ----------------
def calculator(expression):
    try:
        return str(eval(expression))
    except:
        return "Calculation error"

def write_note(text):
    with open(NOTES_FILE, "a", encoding="utf-8") as f:
        f.write(text + "\n")

def read_notes():
    if os.path.exists(NOTES_FILE):
        with open(NOTES_FILE, "r", encoding="utf-8") as f:
            return f.read().strip()
    return ""    

# ---------------- START AGENT ----------------
print("🤖 Agent with PERSISTENT MEMORY start ho gaya hai (exit likhne par band hoga)")

# ---------------- AGENT LOOP ----------------
while True:
    user_input = input("Tum: ")

    # EXIT
    if user_input.lower() == "exit":
        print("Agent band ho raha hai 👋")
        break

    # ---------------- TOOL: CALCULATOR ----------------
    if any(op in user_input for op in ["+", "-", "*", "/"]):
        result = calculator(user_input)
        print("🧮 Calculator:", result)
        continue

    # ---------------- MEMORY READ (PEHLE) ----------------
    if "mera naam kya hai" in user_input.lower():
        if "name" in memory:
            print(f"🧠 Tumhara naam {memory['name']} hai")
        else:
            print("🤔 Mujhe abhi tumhara naam nahi pata")
        continue

    # ---------------- MEMORY STORE (BAAD ME) ----------------
    if "mera naam" in user_input.lower():
        words = user_input.split()
        if len(words) >= 3:
            name = words[2]   # "mera naam <name> hai"
            memory["name"] = name
            save_memory(memory)
            print(f"😊 Theek hai {name}, maine yaad rakh liya")
        else:
            print("❌ Naam samajh nahi aaya")
        continue
        # WRITENOTE
    if user_input.lower().startswith("note likho"):
        note = user_input.replace("note likho", "").strip()
        if note:
            write_note(note)
            print("📝 Note saved successfully")
        else:
            print("❌ Kya note likhna hai?")
        continue

    # READ______NOTE
    if "note dikhao" in user_input.lower():
        notes = read_notes()
        if notes:
            print("📖 Your Notes:")
            print(notes)
        else:
            print("📭 Koi notes nahi mile")
        continue
    # ---------------- AI RESPONSE ----------------
    print("AI soch raha hai...")
    reply = ask_ai(user_input)
    print("AI:", reply)






