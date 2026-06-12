import * as vscode from 'vscode';
import axios from 'axios';

const API_URL = "http://127.0.0.1:8000/generate";

export function activate(context: vscode.ExtensionContext) {
	const disposable = vscode.commands.registerCommand(
		'multi-agent-ai-vscode.helloWorld',
		async () => {

			const prompt = await vscode.window.showInputBox({
				placeHolder: "Generate Bubble Sort",
				prompt: "Enter your AI prompt"
			});

			if (!prompt) {
				return;
			}

			try {

				vscode.window.showInformationMessage(
					"Generating code..."
				);

				const response = await axios.post(
					API_URL,
					{
						prompt: prompt
					}
				);

				const generatedCode =
					response.data.code;

				const editor =
					vscode.window.activeTextEditor;

				if (!editor) {

					vscode.window.showErrorMessage(
						"No active editor found."
					);

					return;
				}

				editor.edit(
					editBuilder => {

						editBuilder.insert(
							editor.selection.active,
							generatedCode
						);

					}
				);

			}
			catch (error) {

				vscode.window.showErrorMessage(
					"Failed to connect to backend."
				);

			}

		}
	);

	context.subscriptions.push(
		disposable
	);

}

export function deactivate() {}