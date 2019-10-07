# Artifact for draft paper "Model-View-Update-Communicate: Session Types meet the Elm Architecture"

Simon Fowler, 4th October 2019

## Introduction

This is the artifact for Model-View-Update-Communicate: Session Types meet the Elm Architecture.

The artifact structure and packaging is based on the artifact for "Exceptional
Asynchronous Session Types: Session Types without Tiers" by Simon Fowler, Sam
Lindley, J. Garrett Morris, and Sara Decova.

The artifact contains the Links programming language extended with a linear MVU
library, along with several example applications. These are packaged in a Docker
image, and we have included scripts to launch the interpreter and the examples.

We provide several example Links programs:

  * Links implementations of all lambda-MVU programs in the paper
    (examples/paper-examples)

  * examples of incorrect implementations of the 2FA server caught by session types in Links
    (examples/caught-errors)

  * the PingPong example: the implementation using transitions is
    `pingpong.links`, and the implementation without is `pingpong-monolith.links`
    (examples/pingpong)

  * the extended chat server example
    (examples/chatserver)

  * the two factor authentication example: the implementation using transitions
    is `twoFactor.links`, and the implementation without transitions is
    `twoFactorMonolith.links`
    (examples/two-factor)

An overview of the Links syntax can be found in `links/doc/quick-help.pod`.

## Structure

  * `links-docker` contains the files used for the Docker image
  * `links` contains the source code of the Links language
  * `custom-examples` is a folder shared between the host and container, useful
     if you wish to try your own examples
  * `prepare.sh` is a script to prepare the Docker image
  * `cleanup.sh` is a script to remove the image and containers after evaluation
  * `run-chatserver.sh` launches the chat server example
  * `run-two-factor.sh` launches the 2FA example
  * `run-pingpong.sh` launches the PingPong example
  * `run-example.sh` is a interactive script to run individual examples
  * `run-interactive.sh` launches the Links REPL
  * `run-custom.sh` runs a custom example file
  * `run-shell.sh` runs a bash shell for the container

## Changing the port

By default, the Links server will listen on port 8080. If you wish to change
this port to a different value, set the `LINKS_PORT` environment variable:

  export LINKS_PORT=9001

In the remainder of the guide, we will assume the default port of 8080.

## Relationship between lambda-MVU and Links

The Lambda-MVU calculus described in the paper is meant as a core calculus
describing the MVU architecture. In contrast, Links is designed to be used as a
general-purpose programming language. It integrates linearity, polymorphism,
unrestricted types, and session types via an approach based on subkinding, as
pioneered by Mazurak et al. (2012). The core type system of Links with session
types is described by Lindley & Morris (2017).

### Differences between the lambda-MVU and Links

  * The monoidal units `htmlEmpty`, `attrEmpty`, `subEmpty`, and `cmdEmpty` are
    written `LinearMvuHTML.empty`, `LinearMvuAttrs.empty`,
    `LinearMvuSubscriptions.empty`, and `LinearMvuCommands.empty` respectively.

  * Links does not yet support operator overloading, so the monoidal
    concatenation operations for HTML, attributes, subscriptions, and commands
    are written `+*`, `+@`, `+^`, and `+$` respectively. Each require the
    relevant module (e.g., `LinearMvuHTML` for `+*`) to be in scope, which can
    be done using `import LinearMvuHTML;` at the top of the file, and then `open
    LinearMvuHTML;` to bring the module into scope. See the examples for
    details.

  * `htmlText` is written as `textNode(str)`

  * Links supports three ways of writing MVU HTML:
    - The `htmlTag` construct is written as `tag(name, attrs, children)`. As an
      example, we can write a `div` tag with a child text node as:

      ```
      open import LinearMvuHTML;
      import LinearMvuAttrs;

      tag("div", LinearMvuAttrs.empty, textNode("Hello, world!")
      ```

    - The `LinearMvuHTML` module contains pre-made functions for many tags, so
      we can write:

      ```
      div(LinearMvuAttrs.empty, textNode("Hello, world!"))
      ```

    - Finally, Links supports the syntactic sugar in the paper, so you can
      write:

      ```
      vdom
        <div>Hello, world!</div>
      ```

## Sample evaluation workflow

  1. Ensure you have `docker` installed.
     For Ubuntu 18.04, see: https://docs.docker.com/v17.09/engine/installation/linux/docker-ce/ubuntu/

  2. Ensure you have added yourself to the `docker` group: `sudo usermod -a -G
     docker <username>`. You will need to log back in to see the permissions take effect.

  3. Run `./prepare.sh` to install the image and prepare the docker container
     (and you might wish to grab a coffee while this churns through)

  4. Run the chatserver example by invoking `./run-chatserver.sh` and follow the
     instructions in the "Chatserver" section later in this guide
     When you're finished, press Ctrl-C to kill the server process.

  5. Run the 2FA example by invoking `./run-two-factor.sh` and follow the
     instructions in the "Two-factor authentication example" section later in
     this guide.

  6. Run the PingPong example by invoking `./run-pingpong.sh` and follow the
     instructions in the "PingPong" section later in this guide.

  7. Run the smaller examples by invoking `./run-example.sh`. Note that
     the "Distributed Exceptions" examples require navigating to
     `http://localhost:8080` in your browser.

  8. Remove any leftover containers and the image by running
     `./cleanup.sh`

You can also run your own examples by adding the file to the `custom_examples`
directory and running `./run-custom.sh <example file name>`.
For example, try running `./run-custom.sh helloworld.links`.

## Installing Links
We strongly recommend using the Docker image. If you do not wish to use Docker
however, you can install Links from source on an Ubuntu 18.04 install as
follows. From the `links` directory:

  1. Install the system dependencies using `sudo apt install m4 libssl-dev pkg-config`
  2. Install `opam`: https://opam.ocaml.org/doc/Install.html
  3. Run `opam init`
  4. Run `opam switch 4.08.0`
  5. Run ``` eval `opam config env` ``` (backticks around 'opam config env')
  6. Run `opam install dune`
  7. Run `opam pin add links .` to install Links and its dependencies
  8. Use links by invoking `linx`

## Relevant source files

The source can be found in the `links` directory. Relevant source files
you might wish to look at:

  * `links/lib/stdlib/linearMvu.links` -- Main Links library and event loop
  * `links/lib/stdlib/linearMvuX.links` for X in { HTML, Attrs, Subscriptions, Commands } -- Data structures and implementations
  * `links/lib/js/vdom.js` -- JavaScript virtual DOM runtime, called by FFI
  * `links/core/proc.ml` -- server concurrency runtime
  * `links/lib/js/jslib.js` -- client concurrency runtime
  * `links/core/evalir.ml` -- server interpreter

## Running the examples

### Chatserver

To run the chat server example, run
  ```
    ./run-chatserver.sh
  ```

Next, visit `http://localhost:8080` in your browser. You should be able to
create a new room. Now open another browser, and you should be able to join the
room you just created.

### Two-factor authentication example

To run the two-factor authentication example, run

  ```
    ./run-two-factor.sh
  ```

Again, navigate to `http://localhost:8080`.

The correct credentials are `User` and `hunter2`.
You will then be prompted for a key -- the "algorithm" for calculating the
response is just to add one to the challenge key you are presented.

### PingPong

To run the PingPong example, run

  ```
    ./run-pingpong.sh
  ```

In one browser, navigate to `http://localhost:8080/pinger`, and in another,
navigate to `http://localhost:8080/ponger`. Two buttons should appear, and
clicking one should enable the other.

### Smaller examples

Running ./run-example.sh will provide you with an interactive script
allowing you to launch each of the smaller examples. Alternatively, you can run
./run-example.sh with an argument to launch an example by path.

## References

Lindley, S. and Morris, J. G. (2017).
 Lightweight functional session types.
 Behavioural Types: from Theory to Tools, page 265.

Mazurak, K., Zhao, J., and Zdancewic, S. (2010).
 Lightweight linear types in System F°.
 In TLDI, pages 77--88. ACM.

