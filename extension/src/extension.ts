import * as vscode from 'vscode';
import axios from 'axios';

interface RefactorResponse {
    original_code: string;
    refactored_code: string;
    explanation: string;
}

export function activate(context: vscode.ExtensionContext) {
    let disposable = vscode.commands.registerCommand('coderefine-ai.refactor', async () => {
        
        const editor = vscode.window.activeTextEditor;
        if (!editor) {
            vscode.window.showErrorMessage('No active editor found');
            return;
        }

        const document = editor.document;
        const selection = editor.selection;
        const selectedText = document.getText(selection);

        if (!selectedText.trim()) {
            vscode.window.showWarningMessage('Please select some code first.');
            return;
        }

        await vscode.window.withProgress({
            location: vscode.ProgressLocation.Notification,
            title: "Refactoring...",
            cancellable: false
        }, async () => {
            try {
                // 1. Call Backend
                const response = await axios.post<RefactorResponse>('http://127.0.0.1:8000/refactor', {
                    code: selectedText,
                    language: document.languageId,
                    instruction: "Refactor this code."
                });
                
                const newCode = response.data.refactored_code;

                // 2. Format as a Git Merge Conflict
                // VS Code natively recognizes this pattern and provides UI buttons!
                const conflictBlock = 
`<<<<<<< CURRENT CODE
${selectedText}
=======
${newCode}
>>>>>>> GEMINI REFACTOR`;

                // 3. Replace the selection with the Block
                await editor.edit(editBuilder => {
                    editBuilder.replace(selection, conflictBlock);
                });

                // 4. (Optional) Force VS Code to detect the conflict patterns immediately
                // Usually happens automatically, but triggering a save or focus helps.
                
            } catch (error: any) {
                vscode.window.showErrorMessage(`Error: ${error.message}`);
            }
        });
    });

    context.subscriptions.push(disposable);
}

export function deactivate() {}