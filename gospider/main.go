package main

import (
	"gospider/config"
	"gospider/context"
	"gospider/image"
	"gospider/page"
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
		PageState:    map[string]string{},
		PageChannel:  make(chan *page.Page, config.ChannelSize),
		ImageChannel: make(chan *image.Image, config.ChannelSize),
	}, &http.Client{}
}

func main() {
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

	ctx.PageChannel <- &page.Page{Url: config.Root, Parsed: true}
}
