# MCQ Test Feature - User Guide

## 🎯 New Feature: Multiple Choice Questions

I've added an **MCQ Test mode** to your interview bot! Now users can choose between:
- **Text Interview** (original conversational mode)
- **MCQ Test** (multiple choice questions with scoring)

## ✨ Features

### **1. Mode Selection**
- In the sidebar, users can choose between:
  - 📝 **Text Interview** - Conversational Q&A
  - ✅ **MCQ Test** - Multiple choice questions

### **2. MCQ Test Mode**
- AI generates multiple choice questions with 4 options (A, B, C, D)
- User types their answer (A, B, C, or D)
- Instant feedback: ✅ Correct or ❌ Incorrect
- Explanation provided for each answer
- Automatic scoring

### **3. Real-Time Scoring**
The sidebar shows:
- **Questions**: Number of questions answered
- **Score**: Current score (e.g., 7/10)
- **Progress Bar**: Visual representation of score
- **Accuracy**: Percentage (e.g., 70%)

### **4. Question Format**
Each MCQ question follows this format:
```
Question: What is the output of print(2 ** 3)?
A) 6
B) 8
C) 9
D) 5
```

### **5. Answer Evaluation**
After answering, the AI provides:
- ✅ Correct! or ❌ Incorrect
- The correct answer
- Brief explanation

## 🎮 How to Use

### **Starting an MCQ Test**
1. Login to the app
2. In the sidebar, select **"MCQ Test"** mode
3. Choose your **Topic** (Python, Java, etc.)
4. Select **Difficulty** level
5. The test starts automatically

### **Answering Questions**
1. Read the question and options
2. Type your answer in the chat input: `A`, `B`, `C`, or `D`
3. Press Enter
4. Get instant feedback
5. Next question appears automatically

### **Viewing Your Score**
- Check the sidebar for real-time score updates
- Score format: `7/10` (7 correct out of 10 questions)
- Progress bar shows visual representation
- Accuracy percentage displayed

### **Ending the Test**
- Type `quit`, `exit`, or `bye` to end
- Final score will be displayed
- Click "New Interview" to start a new test

## 📊 Scoring System

- **Each correct answer**: +1 point
- **Incorrect answer**: 0 points
- **Total questions**: Tracked automatically
- **Accuracy**: (Score / Total Questions) × 100%

## 🎯 Example Session

```
🤖 AI: Question: What is the output of print(2 ** 3)?
      A) 6
      B) 8
      C) 9
      D) 5

👤 You: B

🤖 AI: ✅ Correct! 
      2 ** 3 means 2 raised to the power of 3, which equals 8.

[Sidebar shows: Score: 1/1, Accuracy: 100%]

🤖 AI: Question: Which data structure uses LIFO?
      A) Queue
      B) Stack
      C) Array
      D) Tree

👤 You: B

🤖 AI: ✅ Correct!
      Stack follows Last-In-First-Out (LIFO) principle.

[Sidebar shows: Score: 2/2, Accuracy: 100%]
```

## 💡 Tips

1. **Read Carefully**: Read all options before answering
2. **Type Clearly**: Just type the letter (A, B, C, or D)
3. **Learn from Mistakes**: Read explanations for wrong answers
4. **Track Progress**: Watch your score in the sidebar
5. **Practice More**: Try different difficulty levels

## 🔄 Switching Modes

You can switch between modes anytime:
- **Text Interview** → **MCQ Test**: Click "New Interview" after switching
- **MCQ Test** → **Text Interview**: Click "New Interview" after switching

## 🎨 Visual Indicators

- **Progress Bar**: Green bar showing your accuracy
- **Score Display**: `X/Y` format (X correct out of Y total)
- **Accuracy**: Percentage with one decimal place
- **Question Counter**: Total questions answered

## ✅ Benefits

- **Objective Evaluation**: Clear right/wrong answers
- **Instant Feedback**: Know immediately if you're correct
- **Score Tracking**: See your progress in real-time
- **Learning**: Explanations help you understand concepts
- **Practice**: Great for exam preparation

Enjoy your new MCQ test feature! 🚀
