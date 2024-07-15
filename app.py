from flask import Flask, request, redirect, url_for, session, render_template
import json
import os

app = Flask(__name__)
app.secret_key = "flaskmultilang"  # Set the secret key for session management

# Define the supported languages
SUPPORTED_LANGUAGES = ["en", "tr", "es"]


def loadTranslations(language):
    """
    Load the translation file for the specified language.
    """
    translationFile = (
        f"translations/{language}.json"  # Define the path to the translation file
    )
    if os.path.exists(translationFile):
        # If the translation file exists, open and load the JSON data
        with open(translationFile, "r") as file:
            translations = json.load(file)
            print(f"Loaded translations for language: {language}")
            return translations
    print(f"No translation file found for language: {language}")
    return {}  # Return an empty dictionary if the translation file does not exist


@app.context_processor
def injectTranslations():
    """
    Inject translations into the template context.
    """
    language = session.get(
        "language", "en"
    )  # Get the current language from the session
    translations = loadTranslations(
        language
    )  # Load the translations for the current language
    print(f"Injecting translations for language: {language}")
    return dict(translations=translations)  # Return the translations as a dictionary


@app.route("/set_language", methods=["POST"])
def setLanguage():
    """
    Set the user's language preference.
    """
    language = request.form.get("language")  # Get the selected language from the form
    match language:
        case lang if lang in SUPPORTED_LANGUAGES:
            session["language"] = (
                language  # Set the session language to the selected language
            )
            print(f"Language set to: {language}")
        case _:
            print(f"Unsupported language selected: {language}")
    return redirect(
        request.referrer or url_for("index")
    )  # Redirect to the previous page or index


@app.before_request
def beforeRequest():
    """
    Set the default language before processing each request.
    """
    if "language" not in session:
        # Check if the user's language is not already set in the session
        browserLanguage = request.headers.get(
            "Accept-Language"
        )  # Get the browser's Accept-Language header
        if browserLanguage:
            # If the Accept-Language header is present, parse the first preferred language
            browserLanguage = browserLanguage.split(",")[0].split("-")[0]
            match browserLanguage:
                case lang if lang in SUPPORTED_LANGUAGES:
                    session["language"] = (
                        lang  # Set the session language to the browser's preferred language
                    )
                    print(f"Browser language detected and set to: {lang}")
                case _:
                    session["language"] = (
                        "en"  # Default to English if the preferred language is not supported
                    )
                    print(
                        f"Browser language '{browserLanguage}' not supported. Defaulting to English."
                    )
        else:
            session["language"] = (
                "en"  # Default to English if the Accept-Language header is not present
            )
            print("No browser language detected. Defaulting to English.")
    else:
        print(f"Language already set in session: {session['language']}")


@app.route("/")
def index():
    """
    Render the index page.
    """
    print("Rendering index page")
    return render_template("index.html")  # Render the index.html template


if __name__ == "__main__":
    print("Starting Flask application")
    app.run(debug=True)  # Run the Flask application in debug mode
