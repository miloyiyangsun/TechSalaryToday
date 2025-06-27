# Configuration Guide

## Environment Variables

This project requires certain environment variables to function properly.

### Required Variables

#### GROQ_API_KEY

- **Description**: API key for Groq translation service
- **How to get**: Visit [Groq Console](https://console.groq.com/keys) to get your free API key
- **Example**: `GROQ_API_KEY=gsk_abc123...`

### Setup Instructions

1. **Create a `.env` file** in the project root directory:

   ```bash
   touch .env
   ```

2. **Add your environment variables** to the `.env` file:

   ```bash
   # Add this line to your .env file
   GROQ_API_KEY=your-actual-groq-api-key-here
   ```

3. **Test the configuration**:
   ```bash
   cd POC/poc_scraper
   python3 test_groq_translation.py
   ```

### Alternative: Export Environment Variables

If you prefer not to use a `.env` file, you can export the variables directly:

```bash
export GROQ_API_KEY=your-actual-groq-api-key-here
```

### Security Notes

- ⚠️ **Never commit API keys to version control**
- ✅ The `.env` file is already in `.gitignore`
- ✅ Use environment variables for all sensitive data
- ✅ Rotate API keys regularly
