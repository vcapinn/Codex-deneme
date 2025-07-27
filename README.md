# Vir Habitus Auto Content System

This example project demonstrates how to automatically create Instagram post content from images stored on Google Drive. The workflow periodically checks a Drive folder, downloads new images and uses OpenAI GPT-4 to generate captions, an aphorism title and five high-engagement hashtags. Generated posts and images are saved under `output/`.

## Setup

1. **Clone this repo on Replit** or your local machine.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file with the following variables:
   ```env
   GOOGLE_SERVICE_ACCOUNT=path/to/service_account.json
   OPENAI_API_KEY=sk-...
   ```
4. Ensure your Google service account has access to the Drive folder ID `1VFt73cldRpKQpgsohdlnBxCZa0nZEfYG`.
5. Run the script:
   ```bash
   python vir_habitus_auto_content_system/main.py
   ```

The script will poll the Drive folder every 5 minutes, generate text for new images and save results in `output/`. Each generated text file follows the pattern `post_X.txt`.

## Advanced Usage

The code can be extended to trigger a Zapier webhook or Instagram Graph API to schedule or publish posts automatically. See `main.py` for where to integrate additional logic after saving each post.
