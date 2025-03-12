import { Client, GatewayIntentBits, Events, Message } from 'discord.js';
import { joinVoiceChannel, getVoiceConnection, createAudioPlayer, createAudioResource } from '@discordjs/voice'
import { addSpeechEvent, SpeechEvents, VoiceMessage } from 'discord-speech-recognition';
import WebSocket from "ws";

import * as dotenv from 'dotenv';
dotenv.config({
    path: '../.env'
});

const client = new Client({
  intents: [
    GatewayIntentBits.GuildVoiceStates,
    GatewayIntentBits.GuildMessages,
    GatewayIntentBits.Guilds,
    GatewayIntentBits.MessageContent,
  ],
});

const GUILD_ID   = '822899213955760180';
const CHANNEL_ID = '1349416171312779395';

let working = false;
let currentSoundInterval: any = 0;
let playGeneratingSound = () => {
  let fp = '../sounds/generating.mp3';
  if(working) {
    let connection = getVoiceConnection(GUILD_ID);
    let player = createAudioPlayer();
    connection?.subscribe(player)
    let res = createAudioResource(fp);
    player.play(res)
  }
}

let websocket = new WebSocket("ws://localhost:8127");

websocket.on('message', data => {
    let json: any = JSON.parse(data.toString());
    
    if(json.wav) {
        console.log('playing')
        let connection = getVoiceConnection(GUILD_ID);
        let player = createAudioPlayer();
        connection?.subscribe(player)
        let res = createAudioResource(`../src/${json.wav}`)
        player.play(res)
        clearInterval(currentSoundInterval)
        working = false;
    }
});

addSpeechEvent(client, {
    "lang": "ru",
    "profanityFilter": false,
    "ignoreBots": false
});

client.on(Events.MessageCreate, (msg: Message) => {
  const voiceChannel = msg.member?.voice.channel;
  if (voiceChannel) {
    joinVoiceChannel({
      channelId: voiceChannel.id,
      guildId: voiceChannel.guild.id,
      adapterCreator: voiceChannel.guild.voiceAdapterCreator,
      selfDeaf: false,
    });
  }
});

client.on(SpeechEvents.speech, (msg: VoiceMessage) => {
  if (!msg.content) return;
  if (!msg.content.toLowerCase().startsWith('катя')) return;

  if(!working) {
      console.log('detected: ' + msg.content)
      websocket.send(Buffer.from(JSON.stringify({
        "type": "respond",
        "message": msg.content
      }), 'utf-8'))
      currentSoundInterval = setInterval(playGeneratingSound, 3500)
      working = true;
      playGeneratingSound()
  }
});

client.on(Events.ClientReady, () => {
  console.log("Ready!");
});

client.login(process.env.DISCORD_TOKEN);
