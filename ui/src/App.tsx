import React, { useState } from 'react';
import {
    Container,
    Box,
    Typography,
    TextField,
    Button,
    FormControl,
    InputLabel,
    Select,
    MenuItem,
    Paper,
    CircularProgress,
    Alert,
} from '@mui/material';
import axios from 'axios';

interface GenerationRequest {
    url: string;
    platform: string;
    form_name: string;
    language: string;
}

function App() {
    const [request, setRequest] = useState<GenerationRequest>({
        url: '',
        platform: '',
        form_name: '',
        language: '',
    });
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [result, setResult] = useState<any>(null);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);
        setError(null);
        setResult(null);

        try {
            const response = await axios.post('http://localhost:8000/generate', request);
            setResult(response.data);
        } catch (err: any) {
            setError(err.response?.data?.detail || 'An error occurred');
        } finally {
            setLoading(false);
        }
    };

    return (
        <Container maxWidth="md">
            <Box sx={{ my: 4 }}>
                <Typography variant="h4" component="h1" gutterBottom>
                    ART Code Generation System
                </Typography>

                <Paper sx={{ p: 3, mb: 3 }}>
                    <form onSubmit={handleSubmit}>
                        <TextField
                            fullWidth
                            label="URL"
                            value={request.url}
                            onChange={(e) => setRequest({ ...request, url: e.target.value })}
                            margin="normal"
                            required
                        />

                        <TextField
                            fullWidth
                            label="Platform"
                            value={request.platform}
                            onChange={(e) => setRequest({ ...request, platform: e.target.value })}
                            margin="normal"
                            required
                        />

                        <TextField
                            fullWidth
                            label="Form Name"
                            value={request.form_name}
                            onChange={(e) => setRequest({ ...request, form_name: e.target.value })}
                            margin="normal"
                            required
                        />

                        <FormControl fullWidth margin="normal" required>
                            <InputLabel>Programming Language</InputLabel>
                            <Select
                                value={request.language}
                                label="Programming Language"
                                onChange={(e) => setRequest({ ...request, language: e.target.value })}
                            >
                                <MenuItem value="python">Python</MenuItem>
                                <MenuItem value="java">Java</MenuItem>
                                <MenuItem value="csharp">C#</MenuItem>
                            </Select>
                        </FormControl>

                        <Button
                            type="submit"
                            variant="contained"
                            color="primary"
                            fullWidth
                            sx={{ mt: 2 }}
                            disabled={loading}
                        >
                            {loading ? <CircularProgress size={24} /> : 'Generate Code'}
                        </Button>
                    </form>
                </Paper>

                {error && (
                    <Alert severity="error" sx={{ mb: 2 }}>
                        {error}
                    </Alert>
                )}

                {result && (
                    <Paper sx={{ p: 3 }}>
                        <Typography variant="h6" gutterBottom>
                            Generation Results
                        </Typography>
                        <pre style={{ overflow: 'auto' }}>
                            {JSON.stringify(result, null, 2)}
                        </pre>
                    </Paper>
                )}
            </Box>
        </Container>
    );
}

export default App; 