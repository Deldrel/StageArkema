import openai
import boto3
import json
import speech_recognition as sr
import pyttsx3


def generateSQL(request):
    openai.api_key = "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"

    params = " knowing these paramameters:" \
             "database name: myDatabase; table name: myTable; " \
             "columns: measure_name, time, measure_value::varchar, measure_value::bigint"

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=request + params,
        temperature=0,
        max_tokens=150,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        stop=["#", ";"]
    )

    return response


def extractLine(OpenAIObject, name):
    return OpenAIObject.get("choices")[0].get(name)


def timestreamQuery(query):
    client = boto3.client(
        'timestream-query',
        region_name='eu-west-1',
        aws_access_key_id='AKIAXFHTLNCOEP4GFGEW',
        aws_secret_access_key='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'
    )
    results = client.query(QueryString=query)
    return results


def speakText(command):
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()


def listen():
    r = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration=1)

            audio_data = r.record(source, duration=5)

            print("Recognizing...")

            text = r.recognize_google(audio_data)
            print(text)

            speakText(text)
            return text

    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))

    except sr.UnknownValueError:
        print("unknown error occurred")


if __name__ == "__main__":

    for i in range(1):
        #prompt = listen()
        prompt = "requête sql pour avoir la dernière température"
        prompt = prompt.lower()

        if "sql" in prompt:
            print("Asking openai to generate response...")
            response = generateSQL(prompt)
            # print(response)

            query = extractLine(response, "text")
            print(query)

            results = json.dumps(timestreamQuery(query), indent=4)
            # print(results)

            data = json.loads(results)
            data = data["Rows"][0]["Data"][0]["ScalarValue"]
            print("\nData = " + data)

            speakText("La valeur demandée est " + data)
