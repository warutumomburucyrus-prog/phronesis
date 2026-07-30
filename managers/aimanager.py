import json
import os

from dotenv import load_dotenv
from google import genai
from managers.profilemanager import ProfileManager

AI_MODEL = "gemini-3.1-flash-lite"

class AIManager:

    def __init__(self):

        load_dotenv()

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise Exception("GEMINI_API_KEY not found in .env")

        self.client = genai.Client(
            api_key=api_key
        )

        self.data_folder = "data"

        self.profile_manager = ProfileManager()



    def load_json(self, filename):

        path = os.path.join(
            self.data_folder,
            filename
        )

        if not os.path.exists(path):
            return []

        with open(path, "r") as file:
            return json.load(file)



    def collect_student_facts(self):

        return {

            "courses": self.load_json("courses.json"),
            "exams": self.load_json("exams.json"),
            "assignments": self.load_json("assignments.json"),
            "schedule": self.load_json("schedule.json")

        }



    def build_prompt(self, user_request):

        facts = self.collect_student_facts()

        return f"""
You are Phronesis, an AI academic mentor.

Your job is to help students maximize their grades.

Here is everything you currently know about the student.

COURSES
{json.dumps(facts["courses"], indent=2)}

EXAMS
{json.dumps(facts["exams"], indent=2)}

ASSIGNMENTS
{json.dumps(facts["assignments"], indent=2)}

SCHEDULE
{json.dumps(facts["schedule"], indent=2)}

Student Request:
{user_request}

Your tasks:

1. Analyze the student's academic situation.
2. Prioritize urgent work.
3. Create a realistic study schedule.
4. Explain why you chose that schedule.
5. Give practical study advice.
6. Format the answer using headings and bullet points.
"""



    def generate_study_plan(self, user_request):

        prompt = self.build_prompt(user_request)

        try:

            return self.generate(prompt)

        except Exception as e:

            return f"Gemini Error:\n\n{e}"

    def generate_course_topics(self, course):

        profile = self.profile_manager.get_academic_info()

        prompt = f"""
    You are an academic curriculum expert.

    Generate the main topics taught in this university course.

    University:
    {profile["university"]}

    Programme:
    {profile["programme"]}

    Course:
    {course["name"]}

    Course Code:
    {course["course_code"]}

    Return JSON only.

    Format:

    {{
        "topics": [
            "topic 1",
            "topic 2",
            "topic 3"
        ]
    }}

    Only include topics that belong to this specific course.
    """

        response = self.generate(prompt)

        return response
        
    def generate(self, prompt):

        try:

            response = self.client.models.generate_content(

                model=AI_MODEL,

                contents=prompt
            )

            return response.text
        
        except Exception as e:

            return f"Gemini Error:\n\n{e}"

    def generate_course_intelligence(self, course):

        prompt = f"""
    You are an academic curriculum expert.

    Generate learning intelligence for this university course.

    Course:
    {course["name"]}

    Course Code:
    {course["course_code"]}

    Provide JSON only.

    Format:

    {{
        "topics": [
            "topic 1",
            "topic 2"
        ]
    }}

    Make the topics realistic for a university student studying this course.
    """

        response = self.generate(prompt)

        return response

    def enrich_course(self, course_manager, course):

        response = self.generate_course_topics(course)

        data = json.loads(response)

        course_manager.update_course_by_code(
            course["course_code"],
            {
                "topics": data["topics"]
            }
        )

    def summarise_notes(self, text):

        if not text or not text.strip():

            return (
                "Phronesis could not find readable text "
                "in this PDF."
            )

        text = text.strip()

        print(
            "Summary input size:",
            len(text)
        )

        max_chars = 30000

        if len(text) > max_chars:

            text = text[:max_chars]

        prompt = f"""
    You are Phronesis, an AI university study assistant.

    Create a clear, accurate revision guide from the study notes below.

    IMPORTANT:
    - Summarise ONLY information contained in the notes.
    - Do not invent facts.
    - Do not add outside information.
    - Preserve important formulas exactly.
    - Explain what important formulas represent.
    - Preserve important definitions.
    - Identify relationships between concepts.
    - Highlight exam-relevant information.
    - Remove repetition.
    - Make the result useful for university exam revision.

    Organise the response using these sections:

    # Revision Guide

    ## 1. Main Topics

    List the major topics covered.

    ## 2. Important Concepts

    Explain the important concepts clearly.

    ## 3. Key Definitions

    List important definitions.

    ## 4. Key Formulas

    List important formulas and explain what the variables mean.

    ## 5. Important Relationships

    Explain important connections between concepts.

    ## 6. Exam Revision Points

    List the most important things the student should remember.

    Do not create quiz questions.

    Do not say that you are generating a quiz.

    Do not talk about the process of summarising.

    Return ONLY the revision guide.

    STUDY NOTES:

    {text}
    """

        try:

            response = self.client.models.generate_content(
                model=AI_MODEL,
                contents=prompt
            )

            if not response:

                raise ValueError(
                    "Gemini returned no response."
                )

            summary = response.text

            if not summary:

                raise ValueError(
                    "Gemini returned an empty response."
                )

            summary = summary.strip()

            print(
                "Summary output size:",
                len(summary)
            )

            return summary

        except Exception as e:

            print(
                "SUMMARY GEMINI ERROR:",
                repr(e)
            )

            raise

    
    def generate_quiz(
        self,
        notes,
        number=5,
        previous_questions=""
    ):

        max_chars = 30000

        if len(notes) > max_chars:

            notes = notes[:max_chars]

        print(
            "Quiz input size:",
            len(notes)
        )

        # -----------------------------------------
        # PREVIOUS QUESTIONS
        # -----------------------------------------

        if previous_questions and previous_questions.strip():

            previous_questions_section = f"""
    PREVIOUSLY ASKED QUESTIONS:

    {previous_questions}

    IMPORTANT:
    These questions have ALREADY been given to the student.

    You MUST NOT:

    - repeat any of these questions
    - slightly reword any of these questions
    - create a question that tests the exact same thing
    - change only the names, numbers, or wording of a previous question
    - create a question whose answer is essentially the same as a previous question

    Every new question must test a DIFFERENT aspect of the study material.

    You should deliberately choose different concepts, relationships,
    applications, examples, definitions, calculations, or reasoning
    than those represented by the previous questions.

    If a concept has already been tested, find another concept from the
    notes instead.

    Do NOT guess whether a question is different.

    Actually compare every generated question against the previous
    questions before returning the quiz.

    """
        else:

            previous_questions_section = """
    There are no previous questions.

    You may use any relevant concepts from the study material.
    """

        # -----------------------------------------
        # PROMPT
        # -----------------------------------------

        prompt = f"""
    You are Phronesis, an AI university tutor.

    Create a NEW quiz from the study notes below.

    {previous_questions_section}

    Every question MUST include:

    - course
    - topic
    - difficulty
    - question
    - type
    - options (only for multiple choice)
    - answer
    - explanation

    The "course" field must be:

    "Unknown Course"

    The "topic" field MUST be taken from the study material.

    The topic must identify the actual concept being tested.

    Do not invent information.

    Do not guess information that is not supported by the notes.

    Rules:

    - Create exactly {number} questions.
    - Mix difficulty levels.
    - Include multiple choice and short answer questions.
    - Provide answers.
    - Focus on exam-relevant concepts.
    - Every question must test meaningful knowledge from the notes.
    - Do not repeat questions.
    - Do not create near-duplicate questions.
    - Do not simply change the wording of another question.
    - Do not test the same fact repeatedly.
    - Prefer coverage of different concepts across the quiz.

    The "topic" field is REQUIRED because Phronesis uses it
    to track student progress.

    Never use "unknown".

    Never leave the topic empty.

    The explanation must explain why the answer is correct.

    For multiple choice questions:

    - type must be "multiple_choice"
    - provide exactly 4 options
    - only one option should be correct

    For short answer questions:

    - type must be "short_answer"
    - do not include an options field

    Before returning the quiz, perform a final duplicate check.

    For EACH generated question:

    1. Compare it with every previous question.
    2. Determine whether it tests substantially the same knowledge.
    3. Compare it with every other question in the NEW quiz.
    4. Remove or replace any duplicate or near-duplicate question.
    5. Make sure the final questions cover different concepts.

    Return ONLY valid JSON.

    Required format:

    [
        {{
            "course": "Unknown Course",
            "topic": "Topic name",
            "difficulty": "medium",
            "question": "Question text",
            "type": "multiple_choice",
            "options": [
                "Option A",
                "Option B",
                "Option C",
                "Option D"
            ],
            "answer": "Correct option",
            "explanation": "Why the answer is correct."
        }}
    ]

    STUDY NOTES:

    {notes}
    """

        # -----------------------------------------
        # GENERATE
        # -----------------------------------------

        response = self.client.models.generate_content(
            model=AI_MODEL,
            contents=prompt
        )

        quiz = response.text

        quiz = quiz.replace(
            "```json",
            ""
        )

        quiz = quiz.replace(
            "```",
            ""
        )

        quiz = quiz.strip()

        # -----------------------------------------
        # VALIDATE JSON
        # -----------------------------------------

        try:

            data = json.loads(
                quiz
            )

            if not isinstance(
                data,
                list
            ):

                raise ValueError(
                    "Quiz response is not a JSON list."
                )

            if len(data) != number:

                raise ValueError(
                    f"Expected {number} questions, "
                    f"but Gemini returned {len(data)}."
                )

            # -----------------------------------------
            # VALIDATE QUESTIONS
            # -----------------------------------------

            seen_questions = set()

            for question in data:

                required_fields = [
                    "course",
                    "topic",
                    "difficulty",
                    "question",
                    "type",
                    "answer",
                    "explanation"
                ]

                for field in required_fields:

                    if field not in question:

                        raise ValueError(
                            f"Question is missing required field: {field}"
                        )

                question_text = (
                    question["question"]
                    .strip()
                    .lower()
                )

                if question_text in seen_questions:

                    raise ValueError(
                        "Gemini returned duplicate questions "
                        "within the same quiz."
                    )

                seen_questions.add(
                    question_text
                )

                if question["type"] == "multiple_choice":

                    if len(
                        question.get(
                            "options",
                            []
                        )
                    ) != 4:

                        raise ValueError(
                            "A multiple-choice question "
                            "must have exactly 4 options."
                        )

                elif question["type"] != "short_answer":

                    raise ValueError(
                        f"Invalid question type: "
                        f"{question['type']}"
                    )

            return json.dumps(
                data
            )

        except json.JSONDecodeError as e:

            raise ValueError(
                f"Gemini returned invalid quiz JSON:\n\n"
                f"{quiz}\n\n"
                f"JSON error: {e}"
            )

        except Exception:

            raise

        
    def evaluate_short_answer(
        self,
        question,
        correct_answer,
        user_answer
    ):

        prompt = f"""
You are Phronesis, an AI university tutor evaluating a student's
short-answer response.

Question:
{question}

Expected answer:
{correct_answer}

Student's answer:
{user_answer}

Evaluate the student's answer based on its meaning, not exact wording.

Rules:

1. Decide whether the student's answer is:
   - correct
   - partially_correct
   - incorrect

2. Equivalent wording should be accepted.

3. Different wording should NOT be rejected if it expresses the
   same mathematical or academic concept.

4. If the student says they do not know, cannot answer, or gives
   an irrelevant response, mark it incorrect.

5. Give a concise explanation of the evaluation.

6. If the answer is partially correct, explain what part is correct
   and what is missing.

Return ONLY valid JSON.

Format:

{{
    "result": "correct",
    "feedback": "The student's answer expresses the same idea as the expected answer."
}}

Possible result values:

"correct"
"partially_correct"
"incorrect"
"""

        response = self.client.models.generate_content(
            model=AI_MODEL,
            contents=prompt
        )

        result = response.text

        result = result.replace("```json", "")
        result = result.replace("```", "")
        result = result.strip()

        try:

            data = json.loads(result)

            if data.get("result") not in [
                "correct",
                "partially_correct",
                "incorrect"
            ]:
                raise ValueError(
                    "Invalid evaluation result."
                )

            return data

        except json.JSONDecodeError as e:

            raise ValueError(
                f"Gemini returned invalid evaluation JSON:\n\n"
                f"{result}\n\n"
                f"JSON error: {e}"
            )
