import { Client, GatewayIntentBits, Events, Message } from 'discord.js';
import { joinVoiceChannel, getVoiceConnection, createAudioPlayer, createAudioResource, JoinVoiceChannelOptions, CreateVoiceConnectionOptions } from '@discordjs/voice'
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

import * as config from "../botconfig.json";

const GUILD_ID   = config.GUILDID;
const CHANNEL_ID = config.CHANNELID;

let working = false;
let currentSoundInterval: any = 0;

let listeningModes: any = {};

let playGeneratingSound = () => {
  if(working) {
    let connection = getVoiceConnection(GUILD_ID);
    let player = createAudioPlayer();
    connection?.subscribe(player)
    let res = createAudioResource(config.generatingsound);
    player.play(res)
  }
}

let playListeningSound = () => {
  if(!working) {
    let connection = getVoiceConnection(GUILD_ID);
    let player = createAudioPlayer();
    connection?.subscribe(player);
    let res = createAudioResource(config.listeningsound)
    player.play(res);
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

addSpeechEvent(client, config.sttconfig);

client.on(SpeechEvents.speech, (msg: VoiceMessage) => {
  if (!msg.content) return;

  if(listeningModes[msg.author.id]) {
    listeningModes[msg.author.id] = false
  } else {
    if (!msg.content.toLowerCase().startsWith('катя')) return;
  }

  if (msg.content.toLowerCase() == 'катя') {
    listeningModes[msg.author.id] = true
    playListeningSound()
    return;
  }

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
  let options: any = {
    channelId: CHANNEL_ID,
    guildId: GUILD_ID,
    selfDeaf: false,
    selfMute: false
  }
  let guild = client.guilds.cache.get(GUILD_ID);
  if(guild) options.adapterCreator = guild.voiceAdapterCreator;
  joinVoiceChannel(options);
});

client.login(process.env.DISCORD_TOKEN);
