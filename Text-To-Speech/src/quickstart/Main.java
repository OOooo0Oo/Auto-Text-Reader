//
// Copyright (c) Microsoft. All rights reserved.
// Licensed under the MIT license. See LICENSE.md file in the project root for full license information.
//
// <code>
package quickstart;

import java.io.File;
import java.io.FileNotFoundException;
import java.util.Scanner;
import java.util.concurrent.Future;
import com.microsoft.cognitiveservices.speech.*;
import com.microsoft.cognitiveservices.speech.audio.AudioConfig;

/**
 * Quickstart: synthesize speech using the Speech SDK for Java.
 */
public class Main {

    private static String xmlToString(String filePath) {
        File file = new File(filePath);
        StringBuilder fileContents = new StringBuilder((int)file.length());

        try (Scanner scanner = new Scanner(file)) {
            while(scanner.hasNextLine()) {
                fileContents.append(scanner.nextLine() + System.lineSeparator());
            }
            return fileContents.toString().trim();
        } catch (FileNotFoundException ex) {
            return "File not found.";
        }
    }
    /**
     * @param args Arguments are ignored in this sample.
     */
    /*public static void main(String[] args) {
        try {
            // Replace below with your own subscription key
            String speechSubscriptionKey = "6a6d33d49c9947558a3c424286c2550d";
            // Replace below with your own service region (e.g., "westus").
            String serviceRegion = "eastus";

            int exitCode = 1;
            SpeechConfig config = SpeechConfig.fromSubscription(speechSubscriptionKey, serviceRegion);
            assert(config != null);

            SpeechSynthesizer synth = new SpeechSynthesizer(config);
            assert(synth != null);

            System.out.println("Type some text that you want to speak...");
            System.out.print("> ");
            String text = new Scanner(System.in).nextLine();
            //String text = new String("sasidnaio");
            Future<SpeechSynthesisResult> task = synth.SpeakTextAsync(text);
            assert(task != null);

            SpeechSynthesisResult result = task.get();
            assert(result != null);

            if (result.getReason() == ResultReason.SynthesizingAudioCompleted) {
                System.out.println("Speech synthesized to speaker for text [" + text + "]");
                exitCode = 0;
            }
            else if (result.getReason() == ResultReason.Canceled) {
                SpeechSynthesisCancellationDetails cancellation = SpeechSynthesisCancellationDetails.fromResult(result);
                System.out.println("CANCELED: Reason=" + cancellation.getReason());

                if (cancellation.getReason() == CancellationReason.Error) {
                    System.out.println("CANCELED: ErrorCode=" + cancellation.getErrorCode());
                    System.out.println("CANCELED: ErrorDetails=" + cancellation.getErrorDetails());
                    System.out.println("CANCELED: Did you update the subscription info?");
                }
            }

            result.close();
            synth.close();
            
            System.exit(exitCode);
        } catch (Exception ex) {
            System.out.println("Unexpected exception: " + ex.getMessage());

            assert(false);
            System.exit(1);
        }
    }*/
    public static void main(String[] args) {
        SpeechConfig speechConfig = SpeechConfig.fromSubscription("6a6d33d49c9947558a3c424286c2550d", "westus");
        speechConfig.setProperty(
            "SpeechServiceResponse_Synthesis_WordBoundaryEnabled", "false");
        AudioConfig audioConfig = AudioConfig.fromDefaultSpeakerOutput();
        
        SpeechSynthesizer synthesizer = new SpeechSynthesizer(speechConfig, audioConfig);
        String ssml = xmlToString("ssml.xml");
        //System.out.println(ssml);
        //synthesizer
        SpeechSynthesisResult result = synthesizer.SpeakSsml(ssml);
       
        //SpeechSynthesisResult result = synthesizer.SpeakSsml(ssml);
        //synthesizer.SpeakText("Synthesizing directly to speaker output.");
    }
}
// </code>