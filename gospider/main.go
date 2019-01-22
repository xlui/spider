package main

import (
	"gospider/config"
	"gospider/context"
	"log"
	"net/http"
	"os"
)

func initialize() (ctx *context.Context, client *http.Client) {
	err := os.MkdirAll(config.Storage, 0777)
	if err != nil {
		log.Fatalln("Failed to create image folder!", err.Error())
	}

	return &context.Context{
		PageState:    map[string]int{},
		PageChannel:  make(chan *context.Page, config.ChannelSize),
		ImageChannel: make(chan *context.Image, config.ChannelSize),
	}, &http.Client{}
}

func check(err error, msg string) {
	if err != nil {
		log.Fatalln(msg, err.Error())
	}
}

func run() {
	ctx, client := initialize()

	for i := 0; i < config.Fetchers; i++ {
		go func() {
			for pg := range ctx.PageChannel {
				pg.Fetch(ctx, client)
			}
		}()
	}

	for i := 0; i < config.Downloaders; i++ {
		go func() {
			for img := range ctx.ImageChannel {
				img.Download(ctx, client)
			}
		}()
	}

	for i := 0; i < config.Fetchers; i++ {
		go func() {
			for parse := range ctx.ParseChannel {
				parse.Parse(ctx)
			}
		}()
	}

	ctx.PageChannel <- &context.Page{Url: config.Root, Parsed: true}
}
