const express = require('express');
const cors = require('cors');
const axios = require('axios');
const cheerio = require('cheerio');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.static('public'));

// Services
const pythonToJsConverter = require('./services/pythonToJsConverter');
const apiDocParser = require('./services/apiDocParser');
const repositoryFetcher = require('./services/repositoryFetcher');

// Routes
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// Convert Python samples to JavaScript
app.post('/api/convert', async (req, res) => {
    try {
        const { repoUrl, jsLibrary, apiDocsUrl } = req.body;
        
        if (!repoUrl) {
            return res.status(400).json({ error: 'Repository URL is required' });
        }

        console.log('Starting conversion process...');
        console.log('Repo URL:', repoUrl);
        console.log('JS Library:', jsLibrary || '@azure/ai-agents');
        console.log('API Docs URL:', apiDocsUrl);

        // Step 1: Fetch Python samples from repository
        const pythonSamples = await repositoryFetcher.fetchPythonSamples(repoUrl);
        
        // Step 2: Parse API documentation if provided
        let apiMethods = [];
        if (apiDocsUrl) {
            apiMethods = await apiDocParser.parseApiMethods(apiDocsUrl);
        }

        // Step 3: Convert Python samples to JavaScript
        const jsSamples = await pythonToJsConverter.convertSamples(
            pythonSamples, 
            jsLibrary || '@azure/ai-agents',
            apiMethods
        );

        res.json({
            success: true,
            samplesCount: jsSamples.length,
            samples: jsSamples
        });

    } catch (error) {
        console.error('Conversion error:', error);
        res.status(500).json({ 
            error: 'Failed to convert samples', 
            details: error.message 
        });
    }
});

// Download converted samples as ZIP
app.post('/api/download', async (req, res) => {
    try {
        const { samples } = req.body;
        
        if (!samples || !Array.isArray(samples)) {
            return res.status(400).json({ error: 'Invalid samples data' });
        }

        const archiver = require('archiver');
        
        res.setHeader('Content-Type', 'application/zip');
        res.setHeader('Content-Disposition', 'attachment; filename="js-samples.zip"');
        
        const archive = archiver('zip', { zlib: { level: 9 } });
        archive.pipe(res);
        
        // Add each sample file to the archive
        samples.forEach((sample, index) => {
            const filename = sample.originalName 
                ? sample.originalName.replace('.py', '.js')
                : `sample_${index + 1}.js`;
            archive.append(sample.jsCode, { name: filename });
        });
        
        await archive.finalize();
        
    } catch (error) {
        console.error('Download error:', error);
        res.status(500).json({ error: 'Failed to create download' });
    }
});

app.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
});
