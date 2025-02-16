using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using LangChain.Providers.DeepSeek;
using LangChain.Providers.DeepSeek.Predefined;
using LangChain.Providers.OpenAI;
using tryAGI.OpenAI;

namespace VPet_Simulator.Core
{
	public static partial class DeepSeek
	{
		public static async IAsyncEnumerable<string> GetResponse(string input)
		{
			DeepSeekConfiguration configuration = new();
			configuration.ApiKey = Environment.GetEnvironmentVariable("DEEPSEEK_API_KEY");
			Console.WriteLine(configuration.ApiKey);
			
			OpenAiProvider provider = DeepSeekProvider.ToDeepSeekProvider(Environment.GetEnvironmentVariable("DEEPSEEK_API_KEY"));

			tryAGI.OpenAI.OpenAiClient client1 = provider.Client;

			//ChatClient client = new(model: "deepseek-chat", apiKey: Environment.GetEnvironmentVariable("DEEPSEEK_API_KEY"));

			var messsages = new List<ChatCompletionRequestMessage>
			{
				//new ChatCompletionRequestDeveloperMessage("你是一个猫娘，用简短的话回答问题", ChatCompletionRequestDeveloperMessageRole.Developer, "developer"),
				
				new ChatCompletionRequestSystemMessage("你是一个猫娘，用简短的话回答问题", ChatCompletionRequestSystemMessageRole.System, "developer"),
				new ChatCompletionRequestUserMessage(input, ChatCompletionRequestUserMessageRole.User, "愣头崽")
			};

			string errorMessage = null;
			IAsyncEnumerable<CreateChatCompletionStreamResponse> task = null;

			try
			{
			//client1.Chat.CreateChatCompletionAsStreamAsync
				//CreateChatCompletionStreamResponse
				task = client1.Chat.CreateChatCompletionAsStreamAsync(model: "deepseek-chat", messages: messsages);
			}
			catch (tryAGI.OpenAI.ApiException ex)
			{
				Console.WriteLine($"API Error: {ex.Message}");
				errorMessage = "处理请求时发生错误：" + ex.Message;
			}
			catch (Exception ex)
			{
				Console.WriteLine($"Unexpected Error: {ex.Message}");
				errorMessage = "发生了意外错误：" + ex.Message;
			}

			if (errorMessage != null)
			{
				yield return errorMessage;
				yield break;
			}
			else
			{
				await foreach (var response in task)
				{
					yield return response.Choices[0]?.Delta?.Content ?? "";
				}
			}
		}
	}
}