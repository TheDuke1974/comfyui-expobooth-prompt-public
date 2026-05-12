import { app } from "../../scripts/app.js";

app.registerExtension({
    name: "comfyui-expobooth-prompt.ui",

    async beforeRegisterNodeDef(nodeType, nodeData) {
        if (nodeData.name !== "ExpoBoothPromptBuilder") return;

        const onNodeCreated = nodeType.prototype.onNodeCreated;

        nodeType.prototype.onNodeCreated = function () {
            const result = onNodeCreated ? onNodeCreated.apply(this, arguments) : undefined;

            this.title = "📐 ExpoBooth Prompt";
            this.color = "#3B82F6";
            this.bgcolor = "#1E3A8A";

            return result;
        };
    },
});