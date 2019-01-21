package main

import (
	"gospider/config"
	"gospider/context"
	"gospider/image"
	"gospider/page"
	"log"
	"os"
)

func initialize() (ctx *context.Context) {
	err := os.MkdirAll(config.Storage, 0777);
	if err != nil {
		log.Fatalln("Failed to create image folder!", err.Error())
	}

	return &context.Context{
		PageState:    map[string]string{},
		PageChannel:  make(chan *page.Page, config.ChannelSize),
		ImageChannel: make(chan *image.Image, config.ChannelSize),
	}
}

func main() {

}
